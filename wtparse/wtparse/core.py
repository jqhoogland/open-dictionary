from collections import deque
from inspect import classify_class_attrs
from pprint import pp
from typing import Generator, Iterable
from bs4 import BeautifulSoup, NavigableString
from requests import request
from wtparse.wtypes import AllowedPOSHeader

from wtparse.wtypes import LanguageCode, Language
from wtparse.constants import LANGUAGES_TO_NAMES


def get_full_lang(lang: LanguageCode) -> Language:
    # return LANGUAGES_TO_NAMES[lang].capitalize()
    return "English"


def parse_alt_forms(els: list[BeautifulSoup]):
    """Given a list of elements under the "Alternative forms" heading,
    return a list of alternative forms, with links to their pages & optional qualifiers"""
    ul = els[0].find_next_sibling("ul")
    lis = ul.find_all("li")

    def parse_alt_form(li: BeautifulSoup) -> dict:
        a = li.span.a
        alt_form = {
            "href": a["href"],
            "text": a.text,
            "qualifiers": [q.text for q in li.find_all(class_="qualifier-content")],
        }

        if "new" in a.get("class", []):
            alt_form["new"] = True

        return alt_form

    return [parse_alt_form(li) for li in lis]


def parse_subsection(heading: str, els: list[BeautifulSoup]):
    match heading:
        case "Alternative_forms":
            return parse_alt_forms(els)

    return {}


def parse_subsections(
    els: deque[BeautifulSoup], header_name: str = "h2"
) -> dict[AllowedPOSHeader, dict]:
    """Given an "entry" (a flat list of elements "under" a h3 heading),
    return a nested dictionary representing that entry, with section headings as keys."""

    subsections = {}

    # Iterate until we find the first entry heading (an h3)
    while True:
        if not els:
            return subsections

        if els[0].name == "h3":
            break

        els.popleft()

    # E.g.: `<span class="mw-headline" id="Etymology">Etymology</span>``
    subsection_name = els[0].span["id"]
    subsection = []

    for el in els:
        if el.name == "h3" and subsection:
            subsections[subsection_name] = parse_subsection(subsection_name, subsection)
            subsection_name = el.span["id"]
            subsection = []

        subsection.append(el)

    return subsections


def fetch_entry(word: str, lang: LanguageCode) -> BeautifulSoup:
    html_raw = request("get", f"https://{lang}.wiktionary.com/wiki/{word}").text
    doc = BeautifulSoup(html_raw, "html.parser")
    # print(doc.prettify())

    def gen_els_in_section() -> Generator[BeautifulSoup, None, None]:
        section_header = doc.find("span", {"id": get_full_lang(lang)}).findParent("h2")
        # print(section_header.prettify())

        for el in section_header.next_siblings:
            if el.name == "h2":
                break
            yield el

    section = deque(
        (el for el in gen_els_in_section() if not isinstance(el, NavigableString))
    )

    pp([(el.name if el.name else el) for el in section])
    subsections = parse_subsections(section)

    return subsections
