# CHANGELOG.md

Ein einfacher Changelog für die Theater-Engine. Keine Release-Bürokratie; nur wichtige technische Änderungen werden festgehalten.

## Unreleased

### Added

- Internes `DocumentModel` mit sichtbarer Textintegrität und Absatz-/Span-Struktur.
- Style Engine mit YAML-basierten Styles `theater`, `classic` und `minimal`.
- Rendererunabhängiger `FormattingPlan` zwischen `DocumentModel` und späterem Renderer.
- Schlanke Entwicklungsunterlagen und CI-Checks.

### Changed

- Sprecher-Erkennung wurde in einen eigenen Speaker Parser ausgelagert.
- README, ENGINE_SPEC und ROADMAP beschreiben den aktuellen Architekturstand.

### Fixed

- README beschreibt die Formatierungs-CLI nun korrekt als noch nicht implementiert.
- Regression-Tests sichern abgekürzte Sprecher wie `D. a. Moor` ab.
