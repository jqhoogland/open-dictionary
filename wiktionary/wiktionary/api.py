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


import json
from dataclasses import dataclass
from re import M
from typing import Generator, Literal, Protocol, TypedDict

import wikitextparser as wtp
from requests import request

from wiktionary._types import LanguageCode
#
from wiktionary.en.parser import EnParser
from wiktionary.utils import get_full_lang

APIProp = Literal[
    "text",
    "langlinks",
    "categories",
    "categorieshtml",
    "links",
    "templates",
    "images",
    "externallinks",
    "sections",
    "revid",
    "displaytitle",
    "subtitle",
    "headhtml",
    "modules",
    "jsconfigvars",
    "encodedjsconfigvars",
    "indicators",
    "iwlinks",
    "wikitext",
    "properties",
    "limitreportdata",
    "limitreporthtml",
    "parsetree",
    "parsewarnings",
    "parsewarningshtml",
    "headitems",
]


class APIOptions(TypedDict):
    """See the [official API documentation](https://en.wiktionary.org/w/api.php) for more information."""

    props: list[APIProp]
    section: int


Page = dict[APIProp, dict | list | str]


class Parser(Protocol):
    wiki: LanguageCode = "en"
    def parse(self, entry: str) -> dict: ...
    def jsonld(self, entry: str) -> list[dict]: ...


class Entry(Protocol):
    word: str
    lang: str


def get_ontology() -> dict:
    with open("../ontology/ontology.json", "r+") as f:
        return json.load(f)

@dataclass
class WiktionaryClient:
    """
    An API client for [a Wiktionary](https://meta.wikimedia.org/wiki/Wiktionary#List_of_Wiktionaries).

    It takes one argument, a `parser` configured for the language-specific wiki
    you want to use.

    NOTE: Only "en" is currently supported

    Each page consists of multiple entries (for each language), and each entry consists of multiple sections.
    """
    parser: Parser = EnParser

    # pylint: disable=dangerous-default-value
    def fetch_page(self, word: str, opts: APIOptions = {}) -> Page:
        """Retrieves an entire page for a given word (+ metadata)
        """
        url = (
            f"https://{self.parser.wiki}.wiktionary.org/w/api.php?action=parse&page={word}&format=json&prop=wikitext"
            + "&".join(f"{k}={v}" for k, v in opts.items())
        )
        return request("get", url).json()

    def fetch_wikitext(self, word: str) -> str:
        """Retrieves the wikitext for a given word's page.
        """
        data = self.fetch_page(word)
        return data.get("parse", {}).get("wikitext", {}).get("*", "")

    def _fetch_entry_sections(self, word: str, lang: LanguageCode) -> Entry:
        """
        Each entry starts with a `h2` tag. We read all the sections following
        a tag until the next `h2` tag, which marks the start of the next entry.
        """
        page = self.fetch_wikitext(word)
        sections = iter(wtp.parse(page).sections)

        def get_sections() -> Generator[wtp.Section, None, None]:
            # Skip any sections preceding the entry we want
            while next(sections).title != get_full_lang(lang):
                pass

            # Take sections until we encounter the next entry (i.e., new language)
            try:
                while (section := next(sections)).level != 2:
                    yield section
            except StopIteration:
                pass

        # h3 sections are contained under h3 sections
        return [s for s in get_sections() if s.level == 3]  

    def fetch_entry(self, word: str, lang: LanguageCode) -> Entry:
        sections = self._fetch_entry_sections(word, lang)
        return self.parser.parse(word, sections, lang)

    def fetch_jsonld(self, word: str, lang: LanguageCode) -> dict:
        """
        Retrieves a list of JSON-LD triples for a given word's entry (+ context)
        """
        sections = self._fetch_entry_sections(word, lang)
        
        ontology = get_ontology()
        context = ontology["@context"]

        return {
            "@context": {
                "@base": context["@base"],
                "wt": context["wt"],
                "wt-en": context["wt-en"],
                "od": context["od"],
                "temp": "http://www.wiktionary.org/wiki/Template:",
            },
            "@graph": self.parser.jsonld(word, sections, lang)
        }
