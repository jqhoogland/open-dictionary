"""
# Wiktionary API

Wikimedia has an [API](https://en.wiktionary.org/w/api.php?action=help&modules=parse),
which lets you get access to entries in their original high-fidelity [wikitext](https://en.wikipedia.org/wiki/Help:Wikitext). 
Awesome.

The only problem is that you get raw wikitext back. Now, that's nice because there's actually a lot
of structure contained in wikitext. It's just that you have to do the work of parsing it yourself.

There's also a more minimal [REST API](https://www.mediawiki.org/wiki/API:REST_API), 
but we're sticking to the original API because it has extra, already-parsed information, 
which we may come to need.

"""

from dataclasses import dataclass, field
from typing import Any

from requests import request
import wikitextparser as wtp

from wtparse.api.types import APIOptions, APIResponse
from wtparse.api.sections import AltForm, parse_section
from wtparse.utils import get_full_lang, to_snake_case
from wtparse.wtypes import LanguageCode

# pylint: disable=dangerous-default-value
def fetch_page(word: str, wiki: LanguageCode, opts: APIOptions = {}) -> APIResponse:
    """Fetch the wikitext for a given word and language.
    NOTE: `wiki` is the languagecode for the wiktionary language, not the language of `word`.
    """
    url = (
        f"https://{wiki}.wiktionary.org/w/api.php?action=parse&page={word}&format=json&prop=wikitext"
        + "&".join(f"{k}={v}" for k, v in opts.items())
    )
    return request("get", url).json()


def get_entry_sections(
    word: str, wiki: LanguageCode, lang: LanguageCode = "en"
) -> list[wtp.Section]:
    """Fetch and parse the wikitext for a given word, language, and wiki."""
    data = fetch_page(word, wiki)
    wikitext = data["parse"]["wikitext"]["*"]

    def get_sections():
        sections = iter(wtp.parse(wikitext).sections)

        # Skip any sections preceding the entry we want
        while next(sections).title != get_full_lang(lang):
            pass

        # Take sections until we encounter the next entry (i.e., new language)
        while (section := next(sections)).level != 2:
            yield section

    return list(get_sections())


@dataclass
class Entry:
    word: str
    alt_forms: list[AltForm]
    etymology: Any = ""  # Etymology
    pronunciations: Any = field(default_factory=list)  # list[Pronunciation]
    definitions: Any = field(
        default_factory=dict
    )  # dict[AllowedPOSHeader, POSDefinition]

    @classmethod
    def from_wiktionary(
        cls, word, wiki: LanguageCode = "en", lang: LanguageCode = "en"
    ) -> "Entry":
        data = {
            to_snake_case(s.title): parse_section(s, lang)
            for s in get_entry_sections(word, wiki, lang)
        }

        alt_forms = data.pop("alternative_forms", [])
        etymology = data.pop("etymology", "")
        pronunciations = data.pop("alternative_forms", [])

        return Entry(
            word=word,
            alt_forms=alt_forms,
            etymology=etymology,
            pronunciations=pronunciations,
        )


