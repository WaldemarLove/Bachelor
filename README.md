# Bachelorarbeit: Reproduktion von Heuer und Rubner

Zuerst werden die veröffentlichten Ergebnisse von Heuer und Rubner (2014),
„Optimizing the Prediction Process: From Statistical Concepts to the Case Study
of Soccer“, möglichst genau reproduziert. Erst danach erfolgt die Übertragung
auf andere Saisons. Der vorhandene Reproduktionsplan erläutert die Methodik;
die Priorität wurde inzwischen auf die historische Reproduktion gelegt.

## Umgebung

- Windows, Python **3.12.3**, 64 Bit.
- Eigene virtuelle Umgebung im Projektordner: `.venv`.
- Grundlage ist die reguläre lokale Python-Installation, keine Codex-Laufzeit.
- `requirements.txt` hält die tatsächlich installierten Paketversionen fest.
- Neben den Analysepaketen dienen `nbformat` und `nbclient` der technischen
  Prüfung und Ausführung des Notebooks.

## Ordner

| Pfad | Inhalt |
|---|---|
| `data/raw/` | Unveränderte Ausgangsdaten, lokal und von Git ausgeschlossen |
| `data/processed/` | Abgeleitete Daten, ebenfalls standardmäßig lokal |
| `notebooks/` | Erläuterte, ausführbare Berechnungen |
| `src/` | Spätere wiederverwendbare Python-Funktionen |
| `results/figures/` | Erzeugte Diagramme |
| `results/tables/` | Erzeugte Tabellen |

Es wurden noch keine Forschungsdaten geladen und keine Paperformeln implementiert.
Das erste Notebook enthält ausschließlich einen Umgebungstest und künstliche Testdaten.
PDF- und ACSM-Dateien sowie temporäre Quellenextraktionen sind von Git ausgeschlossen.
Ein Git-Remote wurde nicht eingerichtet.

## Einrichtung auf einem neuen Rechner

Python 3.12 installieren und diesen Ordner in VS Code öffnen. Im PowerShell-Terminal
des Projektordners (bei vorhandener `.venv` die erste Zeile überspringen):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

`python` muss dabei auf die gewünschte reguläre Python-Installation zeigen.
Die festgehaltenen Pakete wurden unter Windows mit Python 3.12.3 geprüft.
Eine Aktivierung der Umgebung per PowerShell-Skript ist für diese Befehle nicht nötig.
Es ist keine Änderung der PowerShell-Ausführungsrichtlinie erforderlich.

## Notebook in VS Code öffnen

1. Die empfohlenen Microsoft-Erweiterungen **Python** und **Jupyter** installieren.
2. `Strg+Umschalt+P` → **Python: Select Interpreter** → `.venv\\Scripts\\python.exe`.
   Falls nötig, **Enter interpreter path** verwenden.
3. `notebooks/01_theoretische_reproduktion.ipynb` öffnen.
4. Oben rechts **Select Kernel** → **Python Environments** → die Projekt-`.venv` wählen.
5. **Run All / Alle ausführen** anklicken.

Workspace-Einstellungen setzen den Standardinterpreter, überschreiben aber nicht
zwingend eine früher gespeicherte Auswahl. Der Notebook-Kernel wird separat gewählt.
Die erste Codezelle prüft ausdrücklich, dass sie in der Projekt-`.venv` läuft.
Das Diagramm wird angezeigt und nach `results/figures/umgebungstest.png` gespeichert.
Es ist nur eine technische Prüfung mit künstlichen Daten.

## Paketversionen aktualisieren

Nach bewusst vorgenommenen Paketänderungen erneut prüfen und Versionen festhalten:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 requirements.txt
```

Vor wissenschaftlichen Auswertungen das Notebook immer von oben nach unten ausführen,
damit die Ergebnisse nicht von einem früheren, unsichtbaren Zellzustand abhängen.
