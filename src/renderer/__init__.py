from __future__ import annotations

__all__ = ["RendererError", "WordRenderer"]


def __getattr__(name: str):
    if name == "RendererError":
        from .render_context import RendererError

        return RendererError
    if name == "WordRenderer":
        from .word_renderer import WordRenderer

        return WordRenderer
    raise AttributeError(name)
