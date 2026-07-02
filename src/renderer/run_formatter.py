from __future__ import annotations

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.text.run import Run

from ..style_models import TextStyle


class RunFormattingError(ValueError):
    pass


class RunFormatter:
    def apply(self, run: Run, style: TextStyle) -> None:
        font = run.font
        font.name = style.font_family
        font.size = Pt(style.font_size)
        font.bold = style.bold
        font.italic = style.italic
        font.underline = style.underline
        font.color.rgb = _rgb_color(style.text_color)
        _apply_highlight(run, style.highlight_color)


def _rgb_color(color: str) -> RGBColor:
    return RGBColor.from_string(color.removeprefix("#"))


def _apply_highlight(run: Run, color: str | None) -> None:
    if color is None:
        return
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), color.removeprefix("#"))
    run._element.get_or_add_rPr().append(shading)
