from src.speaker_parser import SpeakerProfile, parse_speaker_line


def test_profile_alias_supports_external_play_specific_names():
    profile = SpeakerProfile(aliases={"Rollenname": "Kanonische Rolle"})

    parsed = parse_speaker_line("Rollenname. Guten Abend.", profile)

    assert parsed == {
        "raw": "Rollenname",
        "canonical": "Kanonische Rolle",
        "stage_inline": "",
        "after": "Guten Abend.",
    }


def test_generic_parser_accepts_uppercase_speaker_label():
    parsed = parse_speaker_line("FIGUR A (leise). Text")

    assert parsed == {
        "raw": "FIGUR A",
        "canonical": "Figur A",
        "stage_inline": "(leise)",
        "after": "Text",
    }
