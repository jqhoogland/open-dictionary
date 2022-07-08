from typing import Any, Literal, Tuple, TypedDict

from wtparse.constants import (
    ALLOWED_POS_HEADERS,
    HAN_CHARS,
    LANGUAGES,
    MORPHEMES,
    OTHER_POS_HEADERS,
    PARTS_OF_SPEECH,
    PHRASES,
    SYMBOLS_AND_CHARS,
)

Word = str
LanguageCode = Any  # Literal[LANGUAGES]
Language = str
PartOfSpeech = Any  # Literal[PARTS_OF_SPEECH]
AllowedPOSHeader = Any  # Literal[ALLOWED_POS_HEADERS]
Morpheme = Any  # Literal[MORPHEMES]
SymbolsAndChar = Any  # Literal[SYMBOLS_AND_CHARS]
Phrase = Any  # Literal[PHRASES]
HanChar = Any  # Literal[HAN_CHARS]
OtherPosHeader = Any  # Literal[OTHER_POS_HEADERS]
