# Datensichtung für das Gespräch mit dem Professor

Stand: 5. November 2026. Ausschließlich Datenaufbereitung und Beschreibung, keine Modellrechnung.

## Fragestellung und Umfang

Wir bereiten zunächst eine torbasierte Datengrundlage vor. Der Untersuchungszeitraum des Papers ist 1995/96–2010/11. Zusätzlich wurde 1994/95 als Vorgeschichte aufgenommen, damit für 1995/96 eine Vorsaison verfügbar wäre. Diese Zusatzsaison ist eine methodisch abgeleitete Ergänzung und kein ausdrücklich genannter Untersuchungsjahrgang des Papers. Beispielsaison bleibt 2007/08.

## Quelle

Repository: https://github.com/footballcsv/deutschland

Gesicherter Stand: `178324626681a9e4c42b81463f59f9c4500dbd53`.

Laut README sind die Daten Public Domain und ein CSV-Export von OpenFootball. Es handelt sich nicht um eine offizielle Bundesliga-Quelle und nicht um die ursprünglichen kicker-Torchancendaten. Die abgerufenen Dateien enthalten ausschließlich erste Bundesliga (`de.1.csv`). Der vom Nutzer verlinkte Ordner 1991/92 dient nur als Fundstelle und ist nicht in der Auswertung enthalten.

Die Originaldateien bleiben unter `data/raw/footballcsv` unverändert. Das Manifest dokumentiert Downloadzeitpunkt, feste Quell-URLs und SHA-256-Prüfsummen. Die Spalten heißen `Matchday`, `Date`, `Team 1`, `FT`, `Team 2`. Interpretation: offizieller Spieltag, Datum, Heimteam, Endstand, Gastteam.

## Ergebnisse der Strukturprüfung

- 17 Saisons, jeweils 306 Spiele und 18 Teams: insgesamt **5.202 Spiele**.
- Davon 4.896 Spiele im Zeitraum 1995/96–2010/11 und 306 zusätzliche Vorsaisonspiele.
- Je Mannschaft und Saison 34 Spiele, davon 17 Heimspiele und 17 Auswärtsspiele.
- Je Mannschaft 17 Spiele pro Saisonhälfte; je Spieltag neun Spiele.
- Alle gerichteten Heim-/Gastpaarungen je Saison eindeutig, keine Selbstpaarungen.
- Keine fehlenden Werte in den geprüften Pflichtspalten; Tore und Datumsangaben konnten eingelesen werden.
- 10.404 Team-Spiel-Zeilen aus zwei Perspektiven pro Spiel; diese sind nicht unabhängige Beobachtungen.
- 32 unterschiedliche Vereinsbezeichnungen im gesamten Zeitraum. Quellbezeichnungen wurden erhalten, nicht ungeprüft zusammengeführt.

Diese Prüfungen bestätigen die interne Struktur, nicht die historische Richtigkeit jedes einzelnen Spiels. Eine unabhängige Gegenprüfung von Resultaten, Spieltagen und Datumsangaben steht noch aus. Ein lesbares Datum allein garantiert nicht, dass es das tatsächliche Austragungsdatum ist.

## Aufbereitung

1. Saison aus dem Dateinamen ergänzen.
2. Datum in ein einheitliches Format überführen, Endstand in Heim- und Gasttore trennen.
3. Tordifferenz aus Heimsicht = Heimtore minus Gasttore; Torsumme = Heimtore plus Gasttore.
4. Ergebnis als H (Heimsieg), D (Remis), A (Auswärtssieg) kennzeichnen.
5. Hinrunde anhand Spieltag 1–17 und Rückrunde anhand 18–34 zuordnen. Nachholspiele nicht anhand der Datumsreihenfolge in eine andere Saisonhälfte verschieben.
6. Pro Spiel zwei Mannschaftsperspektiven mit eigenen Toren und Gegentoren erzeugen.
7. Spiele, Tore und Tordifferenzen pro Team und Halbserie zusammenfassen.

Es erfolgte keine Heimvorteilkorrektur und keine Ersetzung fehlender Modellmerkmale. Es wurden keine Aufsteigerwerte imputiert, Trainingsparameter geschätzt oder Prognosen berechnet. Punkte wurden bewusst noch nicht abgeleitet; bei einer späteren Ergänzung muss die historische Punktewertung berücksichtigt werden.

## Dateien und Vorführung

Das neue Notebook `notebooks/02b_spieldaten_sichtung.ipynb` zeigt eine Originaldatei, die Qualitätsübersicht, verarbeitete Spiele und die zwei Teamperspektiven. Das vorhandene Notebook `02_datenpruefung.ipynb` wurde nicht verändert.

Die abgeleiteten Dateien liegen unter `data/processed/footballcsv`:

| Datei | Eine Zeile entspricht | Zweck |
|---|---|---|
| `matches.csv` | Einem Spiel | Bereinigte Spieldaten mit Herkunft |
| `team_matches.csv` | Einer Mannschaft in einem Spiel | Basis für spätere Teammerkmale |
| `team_halves.csv` | Einer Mannschaft in einer Saisonhälfte | Beschreibende Bilanz |
| `season_quality.csv` | Einer Saison | Vollständigkeits- und Konsistenzprüfungen |
| `team_names.csv` | Einer Vereinsbezeichnung | Übersicht zur späteren Quellenverknüpfung |

Spiel-IDs identifizieren die Zeilen des gesicherten Quellenstands. Für eine neue Repository-Version müssen Änderungen an der Reihenfolge beachtet werden. Alle CSV-Ausgaben verwenden Kommas als Trennzeichen und UTF-8 mit BOM. Fehlende Werte werden nicht stillschweigend zu null gemacht.

## Gegenüber dem Professor zu klären

- Soll zuerst die torbasierte Variante umgesetzt werden, bevor Torchancendaten beschafft werden?
- Soll die historische Parameterschätzung möglichst genau nachvollzogen werden oder zusätzlich ein strikt zeitlich vorwärts gerichteter Test erfolgen?
- Das Paper beschreibt den Ausschluss der vorhergesagten Saison ausdrücklich für die Einzelspielregression. Ob sämtliche Rückrundenergebnisse mit genau derselben Aufteilung erzeugt wurden, ist nicht eindeutig dokumentiert.
- Welche unabhängige Referenz soll für die Datenkontrolle dienen?

Mögliche kurze Beschreibung: Wir haben die Ergebnisdaten für den Paperzeitraum plus eine Vorsaison gesammelt und strukturell geprüft. Daraus entstehen nachvollziehbare Team- und Halbserienbilanzen. Die Daten erlauben eine torbasierte Modellvariante; die eigentliche Chancenmodell-Reproduktion benötigt zusätzlich vergleichbare Torchancendaten.
