# Theater.Formatierung

Eine kleine Engine, die Theatertexte in DOCX-Dateien analysiert, klassifiziert, formatiert und anschließend prüft, ohne den sichtbaren Textinhalt zu verändern.

Das Projekt entsteht anhand von Referenzdokumenten, ist aber als allgemeines Werkzeug für Theatermanuskripte gedacht.

## Grundprinzip

Die Engine arbeitet nicht nach blindem Suchen-und-Ersetzen. Jeder Absatz wird zuerst klassifiziert:

- Aktüberschrift
- Szenenüberschrift
- Ortsangabe
- Figurenname
- Replik
- Regieanweisung
- Seitenmarkierung
- unklare Stelle zur manuellen Prüfung

Erst danach wird formatiert. Wenn ein Absatz nicht sicher erkannt wird, wird er nicht geraten, sondern als Prüffall markiert. Word-Dateien sind schon chaotisch genug, da muss man nicht noch Würfel hineinwerfen.

## Sicherheitsregel

Der sichtbare Text darf sich durch Formatierung nicht verändern. Dafür wird vor und nach jedem Lauf ein SHA-256-Hash über alle Absatztexte gebildet. Wenn der Hash abweicht, gilt die Ausgabe als fehlerhaft.

## Geplante Pipeline

1. DOCX einlesen
2. Absätze klassifizieren
3. Analysebericht schreiben
4. Formatierung anhand fester Regeln anwenden
5. Texthash prüfen
6. Qualitätsbericht schreiben
7. Manuelle Prüffälle ausgeben

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Analyse ausführen

```bash
python -m src.cli analyse samples/die_raeuber.docx --out reports
```

## Formatierung ausführen

```bash
python -m src.cli format samples/die_raeuber.docx --out output/die_raeuber_formatiert.docx --reports reports
```

## Status

Aktuell ist die Projektstruktur angelegt. Als nächstes wird die Klassifikation stabilisiert, dann die Formatierungs-Engine gebaut und mit Tests abgesichert.
