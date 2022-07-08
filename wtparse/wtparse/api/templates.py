from dataclasses import dataclass
from typing import Literal, Protocol
import warnings
import wikitextparser as wtp

from wtparse.wtypes import LanguageCode


class ParsedTemplate(Protocol):
    """Templates are a feature of wikitext for duplicating formatting
    structured content across pages.

    [Read more](https://en.wiktionary.org/wiki/Wiktionary:Templates)."""
    value: str
    type: Literal["word", "qualifier"]


@dataclass
class LinkedWord(ParsedTemplate):
    value: str
    lang: LanguageCode
    type: Literal["linked_word"] = "linked_word"


@dataclass
class Qualifier(ParsedTemplate):
    value: str
    type: Literal["qualifier"] = "qualifier"


def parse_template(template: wtp.Template) -> ParsedTemplate | None:
    match template.normal_name():
        case "l":
            return LinkedWord(
                value=template.arguments[-1].value,
                lang=template.arguments[0].value,
            )
        case "qualifier":
            return Qualifier(value=template.arguments[0].value)

        case "1":
            # Not-yet created entries
            return None

    warnings.warn(f"Template {template} not recognized.")
    return None


def parse_templates(templates: list[wtp.Template]) -> list[dict]:
    return [pt for t in templates if (pt := parse_template(t))]
