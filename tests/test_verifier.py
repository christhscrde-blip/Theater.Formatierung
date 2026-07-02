from pathlib import Path

from docx import Document

from src.verifier import assert_visible_text_unchanged, visible_text_hash


def make_docx(path: Path, paragraphs: list[str]) -> None:
    doc = Document()
    for paragraph in paragraphs:
        doc.add_paragraph(paragraph)
    doc.save(path)


def test_visible_hash_is_stable_for_same_text(tmp_path: Path):
    first = tmp_path / "first.docx"
    second = tmp_path / "second.docx"
    paragraphs = ["FIGUR A.", "Aber ist Euch auch wohl, Vater?"]

    make_docx(first, paragraphs)
    make_docx(second, paragraphs)

    assert visible_text_hash(first) == visible_text_hash(second)
    assert_visible_text_unchanged(first, second)


def test_visible_hash_changes_when_text_changes(tmp_path: Path):
    first = tmp_path / "first.docx"
    second = tmp_path / "second.docx"

    make_docx(first, ["FIGUR A."])
    make_docx(second, ["FIGUR A!"])

    assert visible_text_hash(first) != visible_text_hash(second)
