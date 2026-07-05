from src.classifier import classify_texts
from src.models import ParagraphType


def test_basic_dialogue_classification():
    paragraphs = classify_texts(
        [
            "Erster Akt",
            "1. Szene",
            "Großer Saal im Stadttheater.",
            "FIGUR A.",
            "Aber ist Euch auch wohl, Vater?",
            "FIGUR B (leise).",
            "Nachrichten von meiner Schwester?",
            "Seite 1",
        ]
    )

    assert paragraphs[0].type == ParagraphType.ACT_HEADING
    assert paragraphs[1].type == ParagraphType.SCENE_HEADING
    assert paragraphs[2].type == ParagraphType.LOCATION
    assert paragraphs[3].type == ParagraphType.SPEAKER
    assert paragraphs[3].speaker == "Figur A"
    assert paragraphs[4].type == ParagraphType.REPLIQUE
    assert paragraphs[4].speaker == "Figur A"
    assert paragraphs[5].type == ParagraphType.SPEAKER_WITH_STAGE
    assert paragraphs[5].speaker == "Figur B"
    assert paragraphs[6].type == ParagraphType.REPLIQUE
    assert paragraphs[6].speaker == "Figur B"
    assert paragraphs[7].type == ParagraphType.PAGE_MARKER


def test_speaker_with_replique_is_detected():
    paragraph = classify_texts(["FIGUR A. Ist alles bereit?"])[0]
    assert paragraph.type == ParagraphType.SPEAKER_WITH_REPLIQUE
    assert paragraph.speaker == "Figur A"
    assert "speaker_and_text_same_paragraph" in paragraph.flags


def test_unknown_without_context_requires_review():
    paragraph = classify_texts(["Irgendein einzelner Satz ohne Sprecher."])[0]
    assert paragraph.type == ParagraphType.UNCLASSIFIED
    assert "needs_manual_review" in paragraph.flags


def test_abbreviated_speaker_with_stage_is_detected_without_context_leak():
    paragraph = classify_texts(["FIGUR B (leise)."])[0]

    assert paragraph.type == ParagraphType.SPEAKER_WITH_STAGE
    assert paragraph.speaker == "Figur B"


def test_abbreviated_speaker_with_replique_is_detected():
    paragraph = classify_texts(["FIGUR B: Nachrichten von meiner Schwester?"])[0]

    assert paragraph.type == ParagraphType.SPEAKER_WITH_REPLIQUE
    assert paragraph.speaker == "Figur B"


def test_mixed_case_speaker_without_profile_is_not_guessed():
    paragraph = classify_texts(["Figur A. Text"])[0]

    assert paragraph.type == ParagraphType.UNCLASSIFIED
    assert "needs_manual_review" in paragraph.flags


def test_roman_numeral_act_and_scene_headings_are_detected():
    paragraphs = classify_texts(["I. Akt", "IV. Scene"])

    assert paragraphs[0].type == ParagraphType.ACT_HEADING
    assert paragraphs[1].type == ParagraphType.SCENE_HEADING


def test_scene_numbering_variants_are_detected():
    paragraphs = classify_texts(["2te Szene", "3. Auftritt", "Zweiter Aufzug"])

    assert paragraphs[0].type == ParagraphType.SCENE_HEADING
    assert paragraphs[1].type == ParagraphType.SCENE_HEADING
    assert paragraphs[2].type == ParagraphType.ACT_HEADING


def test_common_ocr_mistakes_in_headings_are_detected_without_text_changes():
    paragraphs = classify_texts(["Seite l", "Erster Akl", "Zweite Scenc"])

    assert paragraphs[0].type == ParagraphType.PAGE_MARKER
    assert paragraphs[1].type == ParagraphType.ACT_HEADING
    assert paragraphs[2].type == ParagraphType.SCENE_HEADING
    assert [paragraph.text for paragraph in paragraphs] == [
        "Seite l",
        "Erster Akl",
        "Zweite Scenc",
    ]


def test_uncommon_speaker_labels_are_detected():
    paragraphs = classify_texts(
        [
            "2. WÄCHTER.",
            "Wer geht da?",
            "DIE KÖNIGIN-MUTTER:",
            "Schweigt!",
        ]
    )

    assert paragraphs[0].type == ParagraphType.SPEAKER
    assert paragraphs[0].speaker == "2. Wächter"
    assert paragraphs[1].type == ParagraphType.REPLIQUE
    assert paragraphs[1].speaker == "2. Wächter"
    assert paragraphs[2].type == ParagraphType.SPEAKER
    assert paragraphs[2].speaker == "Die Königin-Mutter"
    assert paragraphs[3].type == ParagraphType.REPLIQUE
    assert paragraphs[3].speaker == "Die Königin-Mutter"
