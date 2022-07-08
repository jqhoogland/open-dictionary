from typing import Any

# Adjective, Adverb, Ambiposition, Article, Circumposition, Classifier, Conjunction, Contraction, Counter, Determiner, Ideophone, Interjection, Noun, Numeral, Participle, Particle, Postposition, Preposition, Pronoun, Proper noun, Verb

PARTS_OF_SPEECH = (
    "noun",
    "verb",
    "adjective",
    "adverb",
    "determiner",
    "article",
    "preposition",
    "conjunction",
    "proper noun",
)

# Circumfix, Combining form, Infix, Interfix, Prefix, Root, Suffix
MORPHEMES = (
    "letter",
    "character",
    "phrase",
    "proverb",
    "idiom",
    "symbol",
    "syllable",
    "numeral",
    "initialism",
    "interjection",
    "definitions",
    "pronoun",
)

# Diacritical mark, Letter, Ligature, Number, Punctuation mark, Syllable, Symbol
SYMBOLS_AND_CHARS = ("diacritical mark",)

# Phrases: Phrase, Proverb, Prepositional phrase[22]
PHRASES = ("phrase",)
# Han characters and language-specific varieties: Han character, Hanzi, Kanji, Hanja
HAN_CHARS = ("han characters",)
# Other: Romanization, Logogram, Determinative
OTHER_POS_HEADERS = ("romanization",)


ALLOWED_POS_HEADERS = (
    *PARTS_OF_SPEECH,
    *MORPHEMES,
    *SYMBOLS_AND_CHARS,
    *PHRASES,
    *HAN_CHARS,
    *OTHER_POS_HEADERS,
)

Word = str

PartOfSpeech = Any  # Literal[PARTS_OF_SPEECH]
AllowedPOSHeader = Any  # Literal[ALLOWED_POS_HEADERS]
Morpheme = Any  # Literal[MORPHEMES]
SymbolsAndChar = Any  # Literal[SYMBOLS_AND_CHARS]
Phrase = Any  # Literal[PHRASES]
HanChar = Any  # Literal[HAN_CHARS]
OtherPosHeader = Any  # Literal[OTHER_POS_HEADERS]
