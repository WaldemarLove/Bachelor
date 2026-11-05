"""Nachvollziehbare Datensichtung; keine Modellschätzung oder Heimkorrektur."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def aufbereiten():
    raw = ROOT / 'data/raw/footballcsv'
    manifest = json.loads((raw / 'manifest.json').read_text(encoding='utf-8'))
    frames = []
    for source in manifest['files']:
        path = raw / source['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], path
        df = pd.read_csv(path, dtype=str)
        assert list(df.columns) == ['Matchday', 'Date', 'Team 1', 'FT', 'Team 2'], path
        assert not df.isna().any().any(), f'Fehlende Rohwerte: {path}'
        y = source['season_start']
        df['season'] = f'{y}/{str(y + 1)[-2:]}'
        df['source_row'] = df.index + 2
        df['source_file'] = source['file']
        df['source_url'] = source['url']
        df['matchday'] = pd.to_numeric(df['Matchday'], errors='raise').astype(int)
        df['date'] = pd.to_datetime(df['Date'], format='%a %b %d %Y', errors='raise')
        assert df['FT'].str.fullmatch(r'\d+-\d+').all(), f'Unbekanntes Ergebnisformat: {path}'
        scores = df['FT'].str.split('-', expand=True).astype(int)
        df['home_goals'], df['away_goals'] = scores[0], scores[1]
        # Quellnamen erhalten; keine ungesicherten Zusammenführungen von Vereinen.
        df['home_team'] = df['Team 1'].str.strip()
        df['away_team'] = df['Team 2'].str.strip()
        df['match_id'] = [f'DE1-{y}-{i:03d}' for i in range(1, len(df) + 1)]
        df['half'] = df['matchday'].map(lambda d: 'Hinrunde' if d <= 17 else 'Rückrunde')
        df['goal_difference_home'] = df['home_goals'] - df['away_goals']
        df['total_goals'] = df['home_goals'] + df['away_goals']
        df['result'] = df['goal_difference_home'].map(lambda d: 'H' if d > 0 else 'A' if d < 0 else 'D')
        frames.append(df)
    data = pd.concat(frames, ignore_index=True)
    cols = ['match_id', 'season', 'matchday', 'date', 'half', 'home_team', 'away_team',
            'home_goals', 'away_goals', 'goal_difference_home', 'total_goals', 'result',
            'source_file', 'source_row', 'source_url']
    matches = data[cols].copy()
    team_parts = []
    for side, opponent in [('home', 'away'), ('away', 'home')]:
        t = matches[['match_id', 'season', 'date', 'matchday', 'half']].copy()
        t['team'] = matches[f'{side}_team']
        t['opponent'] = matches[f'{opponent}_team']
        t['is_home'] = side == 'home'
        t['goals_for'] = matches[f'{side}_goals']
        t['goals_against'] = matches[f'{opponent}_goals']
        t['goal_difference'] = t['goals_for'] - t['goals_against']
        team_parts.append(t)
    teams = pd.concat(team_parts, ignore_index=True).sort_values(['season', 'team', 'date'])
    summaries = []
    for season, m in matches.groupby('season', sort=True):
        t = teams[teams['season'] == season]
        counts = t.groupby('team').size()
        home = t.groupby('team')['is_home'].sum()
        halves = t.groupby(['team', 'half']).size()
        pairs = m.groupby(['home_team', 'away_team']).size()
        checks = {
            '306_spiele': len(m) == 306,
            '18_teams': len(counts) == 18,
            '34_spiele_je_team': bool(counts.eq(34).all()),
            '17_heimspiele_je_team': bool(home.eq(17).all()),
            '17_spiele_je_halbserie': bool(halves.eq(17).all()) and len(halves) == 36,
            '9_spiele_je_spieltag': set(m.matchday) == set(range(1, 35)) and bool(m.groupby('matchday').size().eq(9).all()),
            'paarungen_eindeutig': len(pairs) == 306 and bool(pairs.eq(1).all()),
            'keine_selbstspiele': bool(m.home_team.ne(m.away_team).all()),
            'keine_fehlenden_werte': not m.isna().any().any(),
            'torbilanz_null': int(t.goal_difference.sum()) == 0,
        }
        summaries.append({'season': season, 'matches': len(m), 'teams': len(counts),
                          'first_date': m.date.min().date().isoformat(),
                          'last_date': m.date.max().date().isoformat(),
                          'total_goals': int(m.total_goals.sum()),
                          'goals_per_match': float(m.total_goals.mean()),
                          **checks, 'all_checks_pass': all(checks.values())})
    summary = pd.DataFrame(summaries)
    # Ausführliche Teamübersicht, keine Prognosemerkmale oder Modellrechnung.
    coverage = teams.groupby(['season', 'team', 'half']).agg(
        matches=('match_id', 'size'), home_matches=('is_home', 'sum'),
        goals_for=('goals_for', 'sum'), goals_against=('goals_against', 'sum'),
        goal_difference=('goal_difference', 'sum')).reset_index()
    names = teams.groupby('team').agg(first_season=('season', 'min'),
                                     last_season=('season', 'max'), seasons=('season', 'nunique')).reset_index()
    out = ROOT / 'data/processed/footballcsv'
    out.mkdir(parents=True, exist_ok=True)
    for name, frame in [('matches', matches), ('team_matches', teams), ('team_halves', coverage),
                        ('season_quality', summary), ('team_names', names)]:
        frame.to_csv(out / f'{name}.csv', index=False, encoding='utf-8-sig', date_format='%Y-%m-%d')
    return matches, teams, summary


if __name__ == '__main__':
    matches, teams, summary = aufbereiten()
    print(summary[['season', 'matches', 'teams', 'total_goals', 'all_checks_pass']].to_string(index=False))
    print(f'Gesamt: {len(matches)} Spiele, {len(teams)} Team-Spiel-Zeilen.')
