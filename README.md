# Schachprogramm in Python

## Beschreibung
Dieses Schachprogramm wurde in Python mit `pygame` entwickelt und ermöglicht das Spielen von Schach gegen einen zufällig ziehenden Computer.
Das Programm verfügt über eine grafische Benutzeroberfläche und die Figuren lassen sich via Drag & Drop bewegen.

## Voraussetzungen
- Python **3.12.3** (wahrscheinlich auch ältere Versionen kompatibel, aber nicht getestet)
- `pygame`-Bibliothek

## Installation
Neben einer kompatiblen Python-Version muss lediglich `pygame` installiert werden.

Installation `pygame`:
```sh
pip install pygame
```

## Start des Programms
Das Programm wird durch Ausführen der `main.py` gestartet:

## Funktionen und Bedienung
Nach dem Start erscheint ein Schachbrett in der Mitte des Bildschirms. Die Figuren können per Drag & Drop gezogen werden.

### Buttons:
Links neben dem Schachbrett befinden sich folgende Buttons:
1. **"Weiß: Mensch" / "Weiß: Computer"**: Wechselt zwischen menschlichem Spieler und Computer für Weiß.
2. **"Schwarz: Mensch" / "Schwarz: Computer"**: Wechselt zwischen menschlichem Spieler und Computer für Schwarz.
3. **"Brett drehen"**: Ändert die Perspektive des Schachbretts.
4. **"Neues Spiel"**: Startet ein neues Spiel, behält aber die aktuellen Einstellungen.
5. **"Beenden"**: Schließt das Programm.

### Spielverlauf
Rechts neben dem Schachbrett wird der Spielverlauf angezeigt.

## Projektstruktur
Das Programm besteht aus mehreren Dateien:
- `board.py` – Enthält die Klasse für einzelne Felder und das Schachbrett
- `game_states_and_settings.py` – Speichert die Einstellungen und den aktuellen Spielzustand
- `check_tests.py` – Enthält alle Prüfungen auf direkte und Abzugsschachs
- `get_moves.py` – Enthält alle Funktionen, die zur Ermittlung aller ausführbaren Züge benötigt werden
- `execute_moves.py` – Enthält alle Funktionen, die zur Ausführung der Züge benötigt werden
- `pieces.py` – Enthält die Klassen für die Schachfiguren
- `gui.py` – Verwaltet die Benutzeroberfläche
- `control.py` – Reagiert auf Benutzeraktionen
- `ai.py` – Wählt einen zufälligen legalen Zug für den Computer
- `pins.py` – Verwaltet Pins, um die legalen Züge effizienter zu berechnen
- `main.py` – Enthält die `pygame`-Hauptschleife
- `Pieces/` – Enthält die Bilder der Schachfiguren
