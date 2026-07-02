# Word Renderer

Der Word Renderer ist die Rendering-Schicht für DOCX-Ausgaben. Er erhält ein geprüftes `DocumentModel` und einen `FormattingPlan` und wendet die dort bereits entschiedenen Styles auf ein DOCX-Dokument an.

## Grenzen

Der Renderer darf:

- Absatzformatierung anwenden
- Run-Formatierung anwenden
- DOCX laden und speichern
- sichtbare Textintegrität prüfen

Der Renderer darf nicht:

- Absätze klassifizieren
- Sprecher erkennen
- Styles entscheiden
- sichtbaren Text verändern
- PDF oder GUI-Funktionalität erzeugen

## Komponenten

- `WordRenderer`: lädt DOCX, validiert Eingaben, rendert Absätze und speichert nur nach Integritätsprüfung.
- `ParagraphRenderer`: setzt Absatzformatierung und ersetzt Runs exakt anhand des `FormattingPlan`.
- `RunFormatter`: setzt Schrift, Größe, Fett/Kursiv/Unterstrichen, Textfarbe und Highlight.
- `RenderContext`: bündelt DOCX-Dokument, `DocumentModel` und `FormattingPlan`.

## Sicherheitsregel

Vor der finalen Ausgabe wird die gerenderte DOCX-Datei mit dem bestehenden Verifier gegen die Eingabedatei geprüft. Wenn der sichtbare Text abweicht, bricht der Renderer ab.
