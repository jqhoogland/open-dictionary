from dataclasses import dataclass, field
from itertools import dropwhile
from pprint import pp
from typing import Any

import wikitextparser as wtp
from more_itertools import first_true
#
from wiktionary._types import LanguageCode
from wiktionary.en.templates.parse import parse_templates
from wiktionary.utils import to_snake_case
from wiktionary.en.constants import AllowedPOSHeader, get_category


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
    lis = uls.items if uls and uls.items else []
    return [parse_alt_form(li) for li in lis if li]



def parse_etymology(section: wtp.Section, **_) -> list[dict]:
    """Parse an etymology section of wikitext."""
    templates = parse_templates(section.contents)

    return templates


def parse_section(
    section: wtp.Section, lang: LanguageCode = "en"
) -> dict | list[dict]:
    """Parse a section of wikitext."""
    if section.title == "Alternative forms":
        return parse_alt_forms(section, lang=lang)
    elif section.title == "Etymology": # TODO: Support for multiple multiple_etymologies
        return parse_etymology(section, lang=lang)
    

    return None


@dataclass
class EnEntry:
    word: str
    lang: LanguageCode
    
    alt_forms: list[AltForm]
    etymology: Any = None  # Etymology
    pronunciations: Any = field(default_factory=list)  # list[Pronunciation]
    glyph_origin: Any = None
    description: Any = None

    definitions: Any = field(
        default_factory=dict
    )  # dict[AllowedPOSHeader, POSDefinition]



class EnParser:
    wiki: LanguageCode = "en"
    
    HEADINGS_BEFORE_DEFS = [
        "Alternative forms",
        "Description",
        "Glyph Origin",
        "Etymology",
        "Pronunciation",
    ]
    HEADINGS_AFTER_DEFS = [
        "Usage notes",
        "Reconstruction notes",
        "Inflection",
        "Declension",
        "Conjugation",
        "Mutation",
        "Quotations",
        "Alternative forms",
        "Alternative reconstructions",
        "Synonyms",
        "Antonyms",
        "Hypernyms",
        "Hyponyms",
        "Meronyms",
        "Holonyms",
        "Troponyms",
        "Coordinate terms",
        "Derived terms",
        "Related terms",
        "Collocations",
        "Descendants",
        "Translations",
        "Trivia",
        "See also",
        "References",
        "Further reading",
        "Anagrams",
    ]   
    @classmethod
    def _parse_def(cls, word: str, section: wtp.Section, lang: LanguageCode) -> EnEntry:
        """Parse a definition section of wikitext."""
        return {
            "category": get_category(section.title)
        }


    @classmethod
    def _parse(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> EnEntry:
        data = {
            s.title: parse_section(s, lang)
            for s in sections
        }
        alt_forms = data.pop("Alternative forms", [])
        etymology = data.pop("Etymology", "")
        pronunciations = data.pop("Pronunciations", [])
        description = data.pop("Description", None)
        glyph_origin = data.pop("Glyph origin", None)

        pp(data)

        return EnEntry(
            word=word,
            lang=lang,
            alt_forms=alt_forms,
            etymology=etymology,
            pronunciations=pronunciations,
            description=description,
            glyph_origin=glyph_origin,
            definitions=[
                cls._parse_def(word, v, lang) for v in data.values() if v
            ],
        )

    @classmethod
    def parse(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> list[EnEntry]:
        """This returns a list of entries (one for each etymology). Often, there will be only one etymology, and thus only one entry."""       
        
        multiple_etymologies = [
            s for s in sections 
            if s.title.startswith("Etymology") and not s == "Etymology"
        ]

        if multiple_etymologies:
            pre_def_sections = [
                s for s in sections if s.title in cls.HEADINGS_BEFORE_DEFS
            ]
            
            def parse_multiple():
                for etymology in multiple_etymologies:
                    # The first subsection is always (hopefully) `None`
                    subsections = etymology.sections[1:]
                    subsections[0].title = "Etymology"  
                    _sections = [*pre_def_sections, *subsections]
                    yield cls._parse(word, _sections, lang)

            return list(parse_multiple())

        return cls._parse(word, sections, lang)
