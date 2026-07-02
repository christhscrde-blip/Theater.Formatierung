from __future__ import annotations

from pathlib import Path

from docx import Document


def paragraph_texts(docx_path: str | Path) -> list[str]:
    doc = Document(str(docx_path))
    return [paragraph.text for paragraph in doc.paragraphs]


def visible_text(docx_path: str | Path) -> str:
    return "\n".join(paragraph_texts(docx_path))
