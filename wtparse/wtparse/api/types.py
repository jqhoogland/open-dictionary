from typing import Literal, TypedDict


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
    # What information to retrieve
    props: list[APIProp]

    # The identifier of the section to retrieve
    # This expects an integer index. It's not very useful because you don't
    # know ahead of time where your language-specific section will be.
    section: int


APIResponse = dict[APIProp, dict | list | str]
