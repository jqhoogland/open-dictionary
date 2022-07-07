from typing import Literal, TypedDict

from wtparse.wtparse.constants import (
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
Language = Literal[LANGUAGES]
PartOfSpeech = Literal[PARTS_OF_SPEECH]
AllowedPOSHeader = Literal[ALLOWED_POS_HEADERS]
Morpheme = Literal[MORPHEMES]
SymbolsAndChar = Literal[SYMBOLS_AND_CHARS]
Phrase = Literal[PHRASES]
HanChar = Literal[HAN_CHARS]
OtherPosHeader = Literal[OTHER_POS_HEADERS]
