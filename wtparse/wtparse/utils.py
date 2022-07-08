from wtparse.constants import LANGUAGES_TO_NAMES
from wtparse.wtypes import Language, LanguageCode


def get_full_lang(lang: LanguageCode) -> Language:
    """Returns a capitalized, English version of the language corresponding to `lang`"""
    return LANGUAGES_TO_NAMES[lang].capitalize()

def to_snake_case(word):
    """Converts a sentence to snake_case"""
    return word.lower().replace(" ", "_")
