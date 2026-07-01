from __future__ import annotations

import hashlib
from pathlib import Path

from docx import Document


def visible_text(docx_path: str | Path) -> str:
    doc = Document(str(docx_path))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def visible_text_hash(docx_path: str | Path) -> str:
    return hashlib.sha256(visible_text(docx_path).encode("utf-8")).hexdigest()


def assert_visible_text_unchanged(before_docx: str | Path, after_docx: str | Path) -> None:
    before = visible_text_hash(before_docx)
    after = visible_text_hash(after_docx)
    if before != after:
        raise ValueError(
            "Der sichtbare Text wurde verändert. "
            f"before={before} after={after}"
        )
