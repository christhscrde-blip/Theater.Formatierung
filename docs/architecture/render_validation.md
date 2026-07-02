# Rendering Validation

Die Rendering Validation prüft einen `FormattingPlan`, bevor ein Renderer ihn verarbeitet. Sie verändert den Plan nicht, sondern akzeptiert ihn mit einem `ValidationReport` oder meldet konkrete Fehler.

## Warum diese Schicht existiert

Der Renderer soll nur noch rendern. Er soll nicht entscheiden, ob ein Plan logisch konsistent ist. Die Validation Layer fängt deshalb kaputte oder unvollständige Pläne ab, bevor DOCX-Schreiblogik ausgeführt wird.

## Pipeline

1. `DocumentModel` wird gebaut und auf sichtbare Textintegrität geprüft.
2. `FormattingPlan` wird aus Modell und Style Engine erzeugt.
3. `validate_formatting_plan(...)` prüft Struktur, Span-Reihenfolge, Styles und Werte.
4. Nur wenn `ValidationReport.valid` wahr ist, darf ein Renderer fortfahren.

## Verantwortlichkeiten

Die Validation Layer prüft ausschließlich Engine-Datenstrukturen:

- Absatz-IDs und Absatzreihenfolge
- Vorhandene Paragraph- und Run-Styles
- Kontinuierliche, nicht überlappende Span-Ranges
- Span-Grenzen innerhalb eines Absatzes
- bekannte Style-IDs
- gültige Alignment-, Farb- und Schriftgrößenwerte
- leere oder beschädigte Pläne

Sie kennt kein `python-docx` und schreibt keine Dateien.
