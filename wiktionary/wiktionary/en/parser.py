from dataclasses import dataclass, field
from itertools import dropwhile
from pprint import pp
from typing import Any, Generator
import warnings

import wikitextparser as wtp
from more_itertools import first_true
#
from wiktionary.types import LanguageCode
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

    def gen_alt_forms() -> Generator[AltForm, None, None]:
        for ul in section.get_lists():
            for li in ul.items:
                templates = parse_templates(li)
                yield AltForm(
                    word=first_true(templates, pred=lambda x: x["name"] == "link"),
                    qualifiers=list(filter(lambda x: x["name"] == "qualifier", templates)),
                )

    return list(gen_alt_forms())



def parse_etymology(section: wtp.Section, **_) -> list[dict]:
    """Parse an etymology section of wikitext."""
    templates = parse_templates(section.contents)

    return templates


def parse_pronunciation(section: wtp.Section, lang: LanguageCode) -> dict:
    """Parse a pronunciation section of wikitext."""
    pp(section.contents)
    def gen_pronunciation():
        for ul in section.get_lists():
            pp(ul)
            for li in ul.items:
                yield parse_templates(li)

    return list(gen_pronunciation())
    


def parse_section(
    section: wtp.Section, lang: LanguageCode = "en"
) -> dict:
    """Parse a section of wikitext."""
    if section.title == "Alternative forms":
        return parse_alt_forms(section, lang=lang)
    elif section.title == "Etymology": # TODO: Support for multiple multiple_etymologies
        return parse_etymology(section, lang=lang)
    elif section.title == "Pronunciation":
        return parse_pronunciation(section, lang=lang)

    warnings.warn(f"Not processed: {section.title}")
    return None



def parse_def_section(section: wtp.Section, lang: LanguageCode) -> dict:
    if section.title == "Usage notes":
        return None

    warnings.warn(f"Not processed: {section.title}")
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
        data = {
            to_snake_case(s.title): parse_def_section(s, lang)
            for s in section.sections if s
        }   

        return {
            "category": get_category(section.title),
            **data
        }


    @classmethod
    def _parse(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> EnEntry:
        data = {
            s.title: parse_section(s, lang)
            for s in sections
        }
        alt_forms = data.pop("Alternative forms", [])
        etymology = data.pop("Etymology", "")
        pronunciations = data.pop("Pronunciation", [])
        description = data.pop("Description", None)
        glyph_origin = data.pop("Glyph origin", None)

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
