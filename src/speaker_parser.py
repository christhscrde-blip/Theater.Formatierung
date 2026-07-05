from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Mapping

CHARACTER_ALIASES: dict[str, str] = {}
GENERIC_SPEAKER_PATTERN = re.compile(
    r"^(?P<raw>(?:\d+\.\s*)?[A-ZÄÖÜ]"
    r"[A-ZÄÖÜ0-9ÄÖÜẞ '\-,]{0,59})"
    r"(?P<stage>\s*\([^)]*\))?\s*[\.:]\s*(?P<after>.*)$"
)


@dataclass(frozen=True)
class SpeakerProfile:
    aliases: Mapping[str, str] = field(default_factory=dict)


DEFAULT_SPEAKER_PROFILE = SpeakerProfile()


def normalize_name(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.strip(".:; ")
    return text.lower()


def parse_speaker_line(
    text: str, profile: SpeakerProfile | None = None
) -> dict[str, str] | None:
    stripped = text.strip()
    speaker_profile = profile or DEFAULT_SPEAKER_PROFILE
    return _parse_profile_speaker(stripped, speaker_profile) or _parse_generic_speaker(
        stripped
    )


def _parse_profile_speaker(text: str, profile: SpeakerProfile) -> dict[str, str] | None:
    lowered = text.lower()
    aliases = {
        normalize_name(alias): canonical for alias, canonical in profile.aliases.items()
    }

    for alias in sorted(aliases, key=len, reverse=True):
        if not lowered.startswith(alias):
            continue

        raw_name = text[: len(alias)].strip()
        remainder = text[len(alias) :]
        match = re.match(
            r"^\s*(?P<stage>\([^)]*\))?\s*[\.:]\s*(?P<after>.*)$",
            remainder,
        )
        if not match:
            continue

        return _speaker_result(
            raw=raw_name,
            canonical=aliases[alias],
            stage_inline=match.group("stage") or "",
            after=match.group("after") or "",
        )

    return None


def _parse_generic_speaker(text: str) -> dict[str, str] | None:
    match = GENERIC_SPEAKER_PATTERN.match(text)
    if not match:
        return None

    raw_name = match.group("raw").strip()
    if not _is_generic_speaker_label(raw_name):
        return None

    return _speaker_result(
        raw=raw_name,
        canonical=_canonical_generic_name(raw_name),
        stage_inline=match.group("stage") or "",
        after=match.group("after") or "",
    )


def _is_generic_speaker_label(raw_name: str) -> bool:
    return raw_name == raw_name.upper() and any(
        character.isalpha() for character in raw_name
    )


def _canonical_generic_name(raw_name: str) -> str:
    return " ".join(_capitalize_name_part(part) for part in raw_name.split())


def _capitalize_name_part(part: str) -> str:
    return "-".join(segment.capitalize() for segment in part.split("-"))


def _speaker_result(
    raw: str, canonical: str, stage_inline: str, after: str
) -> dict[str, str]:
    return {
        "raw": raw.strip(),
        "canonical": canonical.strip(),
        "stage_inline": stage_inline.strip(),
        "after": after.strip(),
    }
