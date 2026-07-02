from __future__ import annotations

from .document_model_types import DocumentModel, DocumentParagraph
from .formatting_plan_models import (
    FormattingPlan,
    FormattingRun,
    ParagraphFormattingPlan,
)
from .models import TextSpan
from .style_engine import StyleEngine


class FormattingPlanError(ValueError):
    pass


def build_formatting_plan(
    document_model: DocumentModel, style_engine: StyleEngine
) -> FormattingPlan:
    _assert_document_model_integrity(document_model)
    paragraphs = tuple(
        _build_paragraph_plan(paragraph, style_engine)
        for paragraph in document_model.paragraphs
    )
    plan = FormattingPlan(
        source_file=document_model.source_file,
        visible_text_sha256=document_model.visible_text_sha256,
        style_name=style_engine.style_sheet.name,
        paragraphs=paragraphs,
    )
    _assert_plan_integrity(plan, document_model)
    return plan


def _build_paragraph_plan(
    paragraph: DocumentParagraph, style_engine: StyleEngine
) -> ParagraphFormattingPlan:
    runs = _build_formatting_runs(paragraph.spans, style_engine)
    paragraph_plan = ParagraphFormattingPlan(
        index=paragraph.index,
        paragraph_type=paragraph.classification.type,
        speaker=paragraph.classification.speaker,
        needs_manual_review=paragraph.needs_manual_review,
        paragraph_style_id=_paragraph_style_id(runs),
        runs=runs,
    )
    if paragraph_plan.reconstructed_text != paragraph.text:
        raise FormattingPlanError(
            f"FormattingPlan integrity error in paragraph {paragraph.index}: "
            "run text does not reconstruct paragraph text"
        )
    return paragraph_plan


def _build_formatting_runs(
    spans: tuple[TextSpan, ...], style_engine: StyleEngine
) -> tuple[FormattingRun, ...]:
    runs: list[FormattingRun] = []
    cursor = 0
    for span_index, span in enumerate(spans):
        end_offset = cursor + len(span.text)
        runs.append(
            _build_formatting_run(
                span_index=span_index,
                span=span,
                style_engine=style_engine,
                start_offset=cursor,
                end_offset=end_offset,
            )
        )
        cursor = end_offset
    return tuple(runs)


def _build_formatting_run(
    span_index: int,
    span: TextSpan,
    style_engine: StyleEngine,
    start_offset: int,
    end_offset: int,
) -> FormattingRun:
    return FormattingRun(
        span_index=span_index,
        span_type=span.type,
        text=span.text,
        style=style_engine.get_style(span.type),
        style_id=span.type.value,
        start_offset=start_offset,
        end_offset=end_offset,
        speaker=span.speaker,
        flags=span.flags,
    )


def _paragraph_style_id(runs: tuple[FormattingRun, ...]) -> str:
    return runs[0].style_id if runs else ""


def _assert_document_model_integrity(document_model: DocumentModel) -> None:
    if not document_model.has_integrity:
        raise FormattingPlanError("DocumentModel integrity check failed")


def _assert_plan_integrity(plan: FormattingPlan, document_model: DocumentModel) -> None:
    if plan.visible_text != document_model.visible_text or not plan.has_integrity:
        raise FormattingPlanError("FormattingPlan visible text integrity check failed")
