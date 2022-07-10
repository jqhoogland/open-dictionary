from dataclasses import dataclass, field
from itertools import dropwhile
import json
import os
from pathlib import Path
from pprint import pp
from typing import Any, Generator
import warnings

import wikitextparser as wtp
from more_itertools import first_true
#
from wiktionary._types import LanguageCode
from wiktionary.en.templates.parse import parse_templates
from wiktionary.en.constants import AllowedPOSHeader, get_category,  ALLOWED_POS_HEADERS
from wiktionary.utils import template_to_dict, transform_template_dict, to_snake_case


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
                    word=first_true(templates, pred=lambda x: x["@id"] == "link"),
                    qualifiers=list(filter(lambda x: x["@id"] == "qualifier", templates)),
                )

    return list(gen_alt_forms())



def parse_etymology(section: wtp.Section, **_) -> list[dict]:
    """Parse an etymology section of wikitext."""
    templates = parse_templates(section.contents)

    return templates


def parse_pronunciation(section: wtp.Section, lang: LanguageCode) -> dict:
    """Parse a pronunciation section of wikitext."""
    def gen_pronunciation():
        for ul in section.get_lists():
            pp(ul)
            for li in ul.items:
                yield parse_templates(li)

    return list(gen_pronunciation())



def _parse_default(section: wtp.Section, lang: LanguageCode) -> dict:
    """Parse a section of wikitext."""    
    return {
        "@id": to_snake_case(section.title),
        "linked": parse_templates(section.contents)
    }

def parse_default(section: wtp.Section, lang: LanguageCode) -> dict:
    """Parse a section of wikitext."""
    warnings.warn(f"Using default processor: {section.title}")
    try:
        category = get_category(section.title)
    except ValueError:
        category = None  

    return {
        **_parse_default(section, lang),
        "category": category,
        "data": section.contents, # TODO: use `plaintext()` (using `contents` for debugging)
    }


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
    elif to_snake_case(section.title) in ALLOWED_POS_HEADERS:
        return {
            "@id": to_snake_case(section.title),
            **parse_def_section(section, lang=lang)
        }
    elif section.title.lower() in ("derived terms", "related terms", "collocations", "synonyms", "antonyms", "hyperonyms", "hyponyms", "collocations", "descendants", "translations", "anagrams"):
        # Add support for converting any child links to the appropriate semantic link.
        return _parse_default(section, lang)
    

    return parse_default(section, lang=lang)


def parse_def_section(section: wtp.Section, lang: LanguageCode) -> list[dict]:

    def parse_def_subsection(subsection: wtp.Section):
        if to_snake_case(subsection.title) in ALLOWED_POS_HEADERS:
            del subsection.title
            section_start = subsection.contents.split("===", maxsplit=1)[0]
            headline, section_start = section_start.split("\n", maxsplit=1)

            lis = [
                li for ul in wtp.parse(section_start).get_lists() 
                for li in ul.items
            ]

            items = [
                {
                    "text": text, 
                    "links": parse_templates(li)
                } for li in lis if (text := wtp.parse(li).plain_text().strip())
            ]

            return {
                "@id": "def",
                "headline": headline,
                "items": items,
            }
        if subsection.title == "Usage notes":
            pass
        elif subsection.title.lower() in ("derived terms", "related terms", "collocations", "synonyms", "antonyms", "hyperonyms", "hyponyms", "collocations", "descendants", "translations", "anagrams"):
            return _parse_default(subsection, lang)

        warnings.warn(f"Definition section not processed: {subsection.title}")

    return {
        res["@id"]: res for s in section.sections 
        if s and s.title and (res := parse_def_subsection(s)) 
        and res.get("@id")
    }

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
            definitions=list(data.values()),
        )

    @classmethod
    def parse(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> list[EnEntry]:
        """This returns a list of entries (one for each etymology). Often, there will be only one etymology, and thus only one entry."""       
        
        multiple_etymologies = [
            s for s in sections if s.title.startswith("Etymology ")
        ]

        if multiple_etymologies:
            other_sections = [
                s for s in sections if not s.title.startswith("Etymology ")
            ]
            
            def parse_multiple():
                for etymology in multiple_etymologies:
                    # The first subsection is always (hopefully) `None`
                    subsections = etymology.sections[1:]
                    subsections[0].title = "Etymology"  
                    _sections = [*other_sections, *subsections]
                    yield cls._parse(word, _sections, lang)

            return list(parse_multiple())

        return cls._parse(word, sections, lang)

    @classmethod
    def jsonld(cls, word: str, sections: list[wtp.Section], lang: LanguageCode) -> dict:
        """This returns JSON-LD triples coresponding to this entry."""
        
        # with open(Path(os.path.dirname(__file__)) / "templates/templates.json", "r+") as f:
        #     transforms = json.load(f)

        return parse_templates("".join((s.contents for s in sections)))

        
