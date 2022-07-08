from dataclasses import dataclass, field
from pprint import pp
from typing import Any, Type

import wikitextparser as wtp
from more_itertools import first_true
#
from wiktionary.en.templates.parse import parse_templates
from wiktionary._types import LanguageCode
from wiktionary.utils import get_full_lang, to_snake_case


@dataclass
class AltForm:
    word: dict
    qualifiers: dict


def parse_alt_forms(
    section: wtp.Section, **_
) -> list[AltForm]:
    """Parse an alternative forms section of wikitext."""

    def parse_alt_form(element: str) -> AltForm | None:
        templates = parse_templates(element)
        return AltForm(
            word=first_true(templates, pred=lambda x: x["name"] == "link"),
            qualifiers=list(filter(lambda x: x["name"] == "qualifier", templates)),
        )

    uls = section.get_lists()
    lis = uls[0].items if uls and uls[0].items else []
    return [parse_alt_form(li) for li in lis if li]



def parse_etymology(section: wtp.Section, **_) -> list[dict]:
    """Parse an etymology section of wikitext."""
    templates = parse_templates(section.contents)
    pp(section.contents)

    return templates


def parse_section(
    section: wtp.Section, lang: LanguageCode = "en"
) -> list[wtp.Section] | None:
    """Parse a section of wikitext."""
    if section.title == "Alternative forms":
        return parse_alt_forms(section, lang=lang)
    elif section.title == "Etymology": # TODO: Support for multiple etymologies
        return parse_etymology(section, lang=lang)
    elif section.title.startswith("Etymology"):
        # Homographs (multiple definitions )
        return []

    return None


@dataclass
class EnEntry:
    word: str
    lang: LanguageCode
    alt_forms: list[AltForm]
    etymology: Any = ""  # Etymology
    pronunciations: Any = field(default_factory=list)  # list[Pronunciation]
    definitions: Any = field(
        default_factory=dict
    )  # dict[AllowedPOSHeader, POSDefinition]


class EnParser:
    wiki: LanguageCode = "en"

    @classmethod
    def parse(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> EnEntry:
        data = {
            to_snake_case(s.title): parse_section(s, lang)
            for s in sections
        }
        alt_forms = data.pop("alternative_forms", [])
        etymology = data.pop("etymology", "")
        pronunciations = data.pop("alternative_forms", [])

        return EnEntry(
            word=word,
            lang=lang,
            alt_forms=alt_forms,
            etymology=etymology,
            pronunciations=pronunciations,
        )
