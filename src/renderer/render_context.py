from __future__ import annotations

from dataclasses import dataclass

from docx.document import Document as DocxDocument

from ..document_model_types import DocumentModel
from ..formatting_plan_models import FormattingPlan


class RendererError(ValueError):
    pass


@dataclass(frozen=True)
class RenderContext:
    docx: DocxDocument
    document_model: DocumentModel
    formatting_plan: FormattingPlan
