from __future__ import annotations

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.text.paragraph import Paragraph

from ..formatting_plan_models import ParagraphFormattingPlan
from ..style_models import TextAlignment, TextStyle
from .render_context import RendererError
from .run_formatter import RunFormatter

ALIGNMENT_MAP = {
    TextAlignment.LEFT: WD_ALIGN_PARAGRAPH.LEFT,
    TextAlignment.CENTER: WD_ALIGN_PARAGRAPH.CENTER,
    TextAlignment.RIGHT: WD_ALIGN_PARAGRAPH.RIGHT,
    TextAlignment.JUSTIFY: WD_ALIGN_PARAGRAPH.JUSTIFY,
}


class ParagraphRenderer:
    def __init__(self, run_formatter: RunFormatter | None = None):
        self._run_formatter = run_formatter or RunFormatter()

    def render(self, paragraph: Paragraph, plan: ParagraphFormattingPlan) -> None:
        _assert_paragraph_text_matches_plan(paragraph, plan)
        paragraph_style = _paragraph_style(plan)
        _apply_paragraph_format(paragraph, paragraph_style)
        _replace_runs(paragraph, plan, self._run_formatter)
        _assert_paragraph_text_matches_plan(paragraph, plan)


def _paragraph_style(plan: ParagraphFormattingPlan) -> TextStyle:
    if not plan.runs:
        raise RendererError(
            f"Paragraph {plan.index} has no formatting runs and cannot be rendered"
        )
    return plan.runs[0].style


def _apply_paragraph_format(paragraph: Paragraph, style: TextStyle) -> None:
    paragraph.alignment = ALIGNMENT_MAP[style.alignment]
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(style.spacing_before)
    paragraph_format.space_after = Pt(style.spacing_after)
    paragraph_format.left_indent = Pt(style.left_indent)
    paragraph_format.right_indent = Pt(style.right_indent)
    paragraph_format.first_line_indent = Pt(style.first_line_indent)
    paragraph_format.line_spacing = style.line_spacing


def _replace_runs(
    paragraph: Paragraph, plan: ParagraphFormattingPlan, run_formatter: RunFormatter
) -> None:
    paragraph.clear()
    for run_plan in plan.runs:
        run = paragraph.add_run(run_plan.text)
        run_formatter.apply(run, run_plan.style)


def _assert_paragraph_text_matches_plan(
    paragraph: Paragraph, plan: ParagraphFormattingPlan
) -> None:
    if paragraph.text != plan.reconstructed_text:
        raise RendererError(
            f"Paragraph {plan.index} text mismatch: renderer would alter visible text"
        )
