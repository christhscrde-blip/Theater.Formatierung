# Arbeitsregeln

Dieses Projekt bearbeitet Theatermanuskripte. Inhaltliche Änderungen am Text sind verboten.

## Wichtigste Regel

Der sichtbare Text einer DOCX-Datei darf durch Formatierung niemals verändert werden.

Vor und nach jeder Formatierung wird ein sichtbarer Texthash geprüft. Wenn der Hash abweicht, ist die erzeugte Datei ungültig.

## Entwicklungsstil

- Kleine Funktionen statt großer Skriptklumpen.
- Jeder Absatz bekommt genau eine Klassifikation.
- Unsichere Fälle werden als `unclassified` oder `needs_manual_review` markiert.
- Nicht raten.
- Tests müssen die Textintegrität prüfen.

## Projektstruktur

- `src/classifier.py`: erkennt Absatztypen
- `src/formatter.py`: wendet Formatregeln auf DOCX an
- `src/verifier.py`: prüft Textintegrität und Warnfälle
- `src/cli.py`: Kommandozeile
- `tests/`: pytest-Tests
- `samples/`: Beispiel-DOCX-Dateien, nicht zwingend im Repo nötig
- `reports/`: erzeugte Prüfberichte, normalerweise nicht committen
- `output/`: erzeugte DOCX-Dateien, normalerweise nicht committen
