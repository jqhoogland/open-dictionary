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

from typing import Literal, TypedDict
from pydantic import BaseModel
import wikitextparser as wtp
from requests import request
from wtparse.api.types import APIOptions, APIResponse
from wtparse.utils import get_full_lang
from wtparse.wtypes import LanguageCode


def fetch_page(word: str, wiki: LanguageCode, opts: APIOptions = {}) -> APIResponse:
    """Fetch the wikitext for a given word and language.
    NOTE: `wiki` is the languagecode for the wiktionary language, not the language of `word`.
    """
    url = (
        f"https://{wiki}.wiktionary.org/w/api.php?action=parse&page=hello&format=json&prop=wikitext"
        + "&".join(f"{k}={v}" for k, v in opts.items())
    )
    return request("get", url).json()


def get_entry_sections(
    word: str, wiki: LanguageCode, lang: LanguageCode = "en"
) -> list[wtp.Section]:
    """Fetch and parse the wikitext for a given word, language, and wiki."""
    data = fetch_page(word, lang)
    wikitext = data["parse"]["wikitext"]["*"]

    def get_sections():
        sections = iter(wtp.parse(wikitext).sections)

        # Skip any sections preceding the entry we want
        while next(sections).title != get_full_lang(lang):
            pass

        # Take sections until we encounter the next entry (i.e., new language)
        while (section := next(sections)).level != 2:
            yield section

    return [s for s in get_sections()]

class AltForm(TypedDict):
    word: str
    qualifiers: list[str]


def parse_alt_forms(
    section: wtp.Section, lang: LanguageCode = "en"
) -> list[wtp.Section]:
    """Parse an alternative forms section of wikitext."""

    def parse_alt_form(li: str) -> AltForm | None:
        return li

    uls = section.get_lists()
    lis = uls[0].items if uls and uls[0].items else []
    return [parse_alt_form(li) for li in lis if li]


def parse_section(section: wtp.Section, lang: LanguageCode = "en") -> list[wtp.Section]:
    """Parse a section of wikitext."""
    match section.title:
        case "Alternative forms":
            return parse_alt_forms(section, lang)

    return None


def get_entry(
    word: str, wiki: LanguageCode, lang: LanguageCode = "en"
) -> list[wtp.Section]:
    return {
        s.title: parse_section(s, lang) for s in get_entry_sections(word, wiki, lang)
    }
