# CONTRIBUTING.md

Dieses Projekt wird schlank gepflegt. Ziel ist eine robuste Theater-Engine, keine große Projektbürokratie.

## Entwicklungsworkflow

1. Kleine, nachvollziehbare Änderungen machen.
2. Neue Features möglichst in einem eigenen Branch entwickeln.
3. Bugs nach Möglichkeit zuerst mit einem Regression-Test absichern.
4. Danach implementieren und die Checks ausführen.
5. Erst mergen, wenn der Branch grün ist.

`main` muss immer grün bleiben. Wenn Codex in einer lokalen Umgebung keine Remotes oder keinen `main`-Branch sieht, soll Codex diesen Umstand dokumentieren und nicht daran scheitern.

## Textintegrität

DOCX-Inhalte sind textkritisch. Sichtbarer Text darf nicht ohne expliziten Auftrag geändert werden. Formatierung darf niemals heimlich Wörter, Satzzeichen, Leerzeichen oder Absätze verändern.

## Checks vor Merge

```bash
git diff --check
PYTHONPATH=. python -m py_compile src/*.py tests/*.py
PYTHONPATH=. pytest -q
```

Diese Checks sind bewusst klein gehalten. Schwerere Tools werden erst ergänzt, wenn sie dem Projekt konkret helfen.
