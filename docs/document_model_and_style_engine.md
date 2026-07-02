# DocumentModel und Style Engine

Diese Notiz hält die neuen internen Bausteine kompakt fest, ohne README oder ENGINE_SPEC unnötig zu vergrößern.

## DocumentModel

Das `DocumentModel` ist die texttreue Übergabeschicht nach dem Einlesen und Klassifizieren. Es speichert Absatztext, genau eine Klassifikation pro Absatz und verlustfreie `TextSpan`-Segmente.

Integritätsregeln:

- Die Verkettung aller Span-Texte eines Absatzes muss exakt den Absatztext rekonstruieren.
- Der sichtbare Gesamttext wird per SHA-256 geprüft.
- Unsichere Absätze bleiben als `unclassified` oder `needs_manual_review` markiert.

## Style Engine

Die Style Engine trennt Formatierungswerte von Python-Code. YAML-Dateien in `styles/` definieren Defaults und optionale Overrides pro `TextSpanType`.

Mitgelieferte Styles:

- `styles/theater.yaml`
- `styles/classic.yaml`
- `styles/minimal.yaml`

Validierung:

- Pflichtfelder müssen nach Defaults vollständig sein.
- Farben müssen `#RRGGBB` verwenden; `highlight_color` darf `null` sein.
- Erlaubte Ausrichtungen sind `left`, `center`, `right` und `justify`.

Der spätere Formatter soll Styles ausschließlich über die Style Engine beziehen und darf dadurch keine Farben, Schriftgrößen oder Abstände hartcodieren.
