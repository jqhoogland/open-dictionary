LANGUAGES_TO_NAMES = {
    "en": "english",
    "es": "spanish",
    "fr": "french",
    "de": "german",
    "it": "italian",
    "pt": "portuguese",
    "ja": "japanese",
    "ko": "korean",
    # 'zh': 'chinese',  # Need to fix different dialects
    "nl": "dutch",
    "sv": "swedish",
    "fi": "finnish",
    "no": "norwegian",
    "da": "danish",
    "is": "icelandic",
    "pl": "polish",
    "hu": "hungarian",
    "cs": "czech",
    "ro": "romanian",
    "ru": "russian",
    "tr": "turkish",
    "hr": "croatian",
    "el": "greek",
    "he": "hebrew",
    "ar": "arabic",
    "hi": "hindi",
    "th": "thai",
    "uk": "ukrainian",
    "id": "indonesian",
    "fa": "persian",
    "bn": "bengali",
    "vi": "vietnamese",
    "sr": "serbian",
    "sk": "slovak",
    "sl": "slovenian",
    "eo": "esperanto",
    "tl": "tagalog",
    "ms": "malay",
    "km": "khmer",
    "lo": "lao",
    "bo": "tibetan",
    "my": "myanmar",
    "ka": "georgian",
    "ti": "tigrinya",
    "gu": "gujarati",
    "kn": "kannada",
    "ml": "malayalam",
    "or": "oriya",
    "pa": "punjabi",
    "as": "assamese",
    "mr": "marathi",
    "sa": "sanskrit",
    "ne": "nepali",
    "ta": "tamil",
    "te": "telugu",
    "si": "sinhala",
    "am": "amhara",
    "kmr": "kurdish",
    "az": "azerbaijani",
}

LANGUAGES = tuple(LANGUAGES_TO_NAMES.keys())

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
SYMBOLS_AND_CHARS = (,s)

# Phrases: Phrase, Proverb, Prepositional phrase[22]
PHRASES = (,)
# Han characters and language-specific varieties: Han character, Hanzi, Kanji, Hanja
HAN_CHARS = (),)
# Other: Romanization, Logogram, Determinative
OTHER_POS_HEADERS = (,)


ALLOWED_POS_HEADERS = tuple(
    *PARTS_OF_SPEECH,
    *MORPHEMES,
    *SYMBOLS_AND_CHARS,
    *PHRASES,
    *HAN_CHARS,
    *OTHER_POS_HEADERS
)
