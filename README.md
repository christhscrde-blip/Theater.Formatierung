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

## Installation

Für die erste Alpha-Version ist eine lokale, editierbare Installation vorgesehen:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -e .
```

Für Entwicklung und Tests können die Test-Abhängigkeiten zusätzlich installiert werden:

```bash
pip install -e '.[dev]'
```

Nach der Installation steht das Konsolenkommando `theater-formatierung` zur Verfügung.

## Quick start

Eine DOCX-Datei kann direkt über die installierte CLI analysiert werden:

```bash
theater-formatierung analyse samples/die_raeuber.docx --out reports
```

Die Formatierungs-Pipeline kann in dieser Alpha außerdem direkt aus Python aufgerufen werden:

```python
from src.pipeline import format_docx

report = format_docx(
    "samples/die_raeuber.docx",
    "output/die_raeuber_formatiert.docx",
)
print(report.visible_text_integrity)
print(report.output_hash)
```

## Format command

Die Formatierungsfunktion schreibt eine neue DOCX-Datei und prüft anschließend, dass der sichtbare Text unverändert geblieben ist:

```python
from src.pipeline import format_docx

report = format_docx("input.docx", "output.docx")
```

Das zurückgegebene `FormattingReport` enthält unter anderem:

- Quelldatei
- Ausgabedatei
- Laufzeit in Sekunden
- Absatzanzahl
- Anzahl manueller Prüffälle
- Anzahl Validierungswarnungen und -fehler
- Ergebnis der sichtbaren Textintegrität
- SHA-256-Hash des sichtbaren Ausgabetextes

## Analyse command

Die installierte CLI analysiert DOCX-Dateien und schreibt Berichte in einen Ausgabeordner:

```bash
theater-formatierung analyse input.docx --out reports
```

Dabei entstehen aktuell:

- `reports/analysis_report.json`
- `reports/paragraph_classification.csv`

## Style selection

Ohne expliziten Stil nutzt `format_docx(...)` den Standardstil `styles/theater.yaml`.
Ein anderer Stil kann als drittes Argument übergeben werden:

```python
from pathlib import Path
from src.pipeline import format_docx

report = format_docx(
    "input.docx",
    "output.docx",
    Path("styles/classic.yaml"),
)
```

Weitere vorhandene Beispielstile liegen in `styles/`, zum Beispiel:

- `styles/theater.yaml`
- `styles/classic.yaml`
- `styles/minimal.yaml`

## Example output

Ein Analyseaufruf gibt den Analysebericht als JSON aus und nennt die geschriebenen Dateien:

```text
{
  "source_file": "input.docx",
  "paragraph_count": 42,
  "type_counts": {
    "speaker": 12,
    "replique": 18,
    "stage_direction": 4
  },
  "manual_review_count": 2,
  "visible_text_sha256": "f2f4..."
}
Analysebericht: reports/analysis_report.json
Absatzklassifikation: reports/paragraph_classification.csv
```

Ein Formatierungslauf über `format_docx(...)` liefert ein `FormattingReport`-Objekt, beispielsweise:

```text
FormattingReport(
    source_file=PosixPath('input.docx'),
    output_file=PosixPath('output.docx'),
    runtime_seconds=0.18,
    paragraph_count=42,
    classified_paragraph_count=42,
    manual_review_count=2,
    validation_warning_count=0,
    validation_error_count=0,
    visible_text_integrity=True,
    output_hash='f2f4...'
)
```

## Status

Die erste Alpha macht das Projekt installierbar und stellt das vorhandene Analysekommando als Konsolenskript bereit. Die Formatierungspipeline ist bereits als Python-API verfügbar und bleibt durch Texthash-Prüfungen abgesichert.
