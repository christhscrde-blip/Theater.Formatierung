from __future__ import annotations

import re

def normalize_name(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.strip(".:; ")
    return text.lower()

        if not lowered.startswith(alias):
            continue

        raw_name = stripped[: len(alias)].strip()
        remainder = stripped[len(alias) :]
        match = re.match(
            r"^\s*(?P<stage>\([^)]*\))?\s*[\.:]\s*(?P<after>.*)$",
            remainder,
        )
        if not match:
            continue