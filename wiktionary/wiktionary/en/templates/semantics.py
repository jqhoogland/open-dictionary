

from wiktionary.en.templates.base import _LANG, COMMON_RENAME, TemplateMapping

Qualifier = TemplateMapping(
    name="qualifier",
    template_names=["qualifier", "qual", "i", "q"],
    variadic_name="qualifiers",
    variadic_start='1',
    variadic_rename={"": "qualifier"},
)


Label = TemplateMapping(
    name="label",
    template_names=["label", "lb", "lbl"],
    rename={"1": _LANG[1]},
    variadic_name="labels",
    variadic_rename={"": "l"},
    extra_transform={"labels": lambda labels: [l["l"] for l in labels]},
)

Gloss = TemplateMapping(
    name="gloss",
    template_names=["gloss", "gl"],
    rename={"1": "gloss"},
)


Sense = TemplateMapping(
    name="sense",
    template_names=["sense", "s"],
    rename={"1": "sense"},
)


Synonym = TemplateMapping(
    name="synonyms",
    template_names=["synonyms", "syn", "synonyms"],
    rename={"1": _LANG[1]},
    variadic_start="1",
    variadic_name="synonyms",
    variadic_rename={"": "synonym", "q": "qualifier", "qq": "qualifier", "g": "gender", **COMMON_RENAME},
)

Antonym = Synonym.copy(
    name="antonyms",
    template_names=["antonym", "ant", "antonyms"]
)


Hypernym = Synonym.copy(
    name="hypernyms",
    template_names=["hypernym", "hyper","hypernyms"]
)

Hyponym = Synonym.copy(
    name="hyponyms",
    template_names=["hyponym", "hypo","hyponyms"]
)

SEMANTIC_TEMPLATES = [
    Qualifier,
    Label,
    Gloss,
    Sense,
    Antonym,
    Hypernym,
    Hyponym,
]
