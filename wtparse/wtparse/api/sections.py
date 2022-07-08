from dataclasses import dataclass

from more_itertools import first_true
import wikitextparser as wtp

from wtparse.api.templates import LinkedWord, Qualifier, parse_templates
from wtparse.wtypes import LanguageCode


@dataclass
class AltForm:
    word: LinkedWord
    qualifiers: list[Qualifier]


def parse_alt_forms(
    section: wtp.Section, **_
) -> list[wtp.Section]:
    """Parse an alternative forms section of wikitext."""

    def parse_alt_form(element: str) -> AltForm | None:
        templates = parse_templates(wtp.parse(element).templates)
        return AltForm(
            word=first_true(templates, pred=lambda x: x.type == "linked_word"),
            qualifiers=list(filter(lambda x: x.type == "qualifier", templates)),
        )

    uls = section.get_lists()
    lis = uls[0].items if uls and uls[0].items else []
    return [parse_alt_form(li) for li in lis if li]


def parse_section(section: wtp.Section, lang: LanguageCode = "en") -> list[wtp.Section]:
    """Parse a section of wikitext."""
    match section.title:
        case "Alternative forms":
            return parse_alt_forms(section, lang=lang)

    return None
