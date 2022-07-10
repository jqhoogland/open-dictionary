from typing import Any, Literal

# Adjective, Adverb, 
PARTS_OF_SPEECH = {
    "noun",
    "verb",
    "adjective",
    "adverb",
    "determiner",
    "article",
    "preposition",
    "conjunction",
    "proper_noun",
    "ambiposition", "circumposition", "classifier", "contraction", "counter",  "ideophone", "interjection",  "numeral", "participle", "particle", "postposition", "pronoun",
}

MORPHEMES = (
    "circumfix", "combining_form", "infix", "interfix", "prefix", "root", "suffix"
)
SYMBOLS_AND_CHARS = ("diacritical_mark", "letter", "ligature", "number", "punctuation_mark", "syllable", "symbol")
PHRASES = ("phrase", "proverb", "prepositional_phrase")
HAN_CHARS = ("han_character", "hanzi", "kanji", "hanja")
OTHER_POS_HEADERS = ("romanization", "logogram", "determinative")


ALLOWED_POS_HEADERS = (
    *PARTS_OF_SPEECH,
    *MORPHEMES,
    *SYMBOLS_AND_CHARS,
    *PHRASES,
    *HAN_CHARS,
    *OTHER_POS_HEADERS,
)

# TODO: Move this all somewhere more sensible

Word = str

PartOfSpeech = Any  # Literal[PARTS_OF_SPEECH]
AllowedPOSHeader = Literal[ALLOWED_POS_HEADERS]
Morpheme = Any  # Literal[MORPHEMES]
SymbolsAndChar = Any  # Literal[SYMBOLS_AND_CHARS]
Phrase = Any  # Literal[PHRASES]
HanChar = Any  # Literal[HAN_CHARS]
OtherPosHeader = Any  # Literal[OTHER_POS_HEADERS]

POSHeaderCategory = Literal["part_of_speech", "morpheme", "symbol_or_char", "phrase", "han_specific", "other"]


def get_category(pos_header: AllowedPOSHeader) -> POSHeaderCategory:
    if pos_header in PARTS_OF_SPEECH:
        return "part_of_speech"
    elif pos_header in MORPHEMES:
        return "morpheme"
    elif pos_header in SYMBOLS_AND_CHARS:
        return "symbol_or_char"
    elif pos_header in PHRASES:
        return "phrase"
    elif pos_header in HAN_CHARS:
        return "han_specific"
    elif pos_header in OTHER_POS_HEADERS:
        return "other"

    raise ValueError(f"Unknown POS header: {pos_header}")
