from dataclasses import dataclass
from pprint import pp

from more_itertools import first_true
import wikitextparser as wtp

from wtparse.templates import Link, Qualifier, parse_templates
from wtparse.wtypes import LanguageCode


@dataclass
class AltForm:
    word: Link
    qualifiers: list[Qualifier]


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


def parse_section(section: wtp.Section, lang: LanguageCode = "en") -> list[wtp.Section]:
    """Parse a section of wikitext."""
    match section.title: 
        case "Alternative forms":
            return parse_alt_forms(section, lang=lang)
        case "Etymology": # TODO: Support for multiple etymologies
            return parse_etymology(section, lang=lang)

    return None
