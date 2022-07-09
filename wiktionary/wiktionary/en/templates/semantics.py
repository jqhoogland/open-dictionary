

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
    rename={"1": _LANG[1], "2": "value"},
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
    template_names=["sense", "s", "senseid", "senseno"],
    rename={"1": "sense"},
)

# Nyms


Nym = TemplateMapping(
    name="nyms",
    template_names=[],
    rename={"1": _LANG[1]},
    variadic_start="2",
    variadic_name="synonyms",
    variadic_rename={"": "synonym", "q": "qualifier", "qq": "qualifier", "g": "gender", **COMMON_RENAME},
)

Synonym = Nym.copy(
    name="synonyms",
    template_names=["synonyms", "syn", "synonyms"],
)


Antonym = Nym.copy(
    name="antonyms",
    template_names=["antonym", "ant", "antonyms"]
)

Hypernym = Nym.copy(
    name="hypernyms",
    template_names=["hypernym", "hyper","hypernyms"]
)

Hyponym = Nym.copy(
    name="hyponyms",
    template_names=["hyponym", "hypo","hyponyms"]
)

Meronym = Nym.copy(
    name="meronyms",
    template_names=["meronym", "mero","meronyms"]
)   

Holonym = Nym.copy(
    name="holonyms",
    template_names=["holonym", "holo","holonyms"]
)   

Troponym = Nym.copy(
    name="troponyms",
    template_names=["troponym", "tropo","troponyms"]
)   

CoordinateTerm = Nym.copy(
    name="coordinate_terms",
    template_names=["coordinate terms", "cot"]
)   

OtherwiseRelated = Nym.copy(
    name="other_rel",
    template_names=["hyponym", "hypo","hyponyms"]
)   


NYMS = [
    Synonym,
    Antonym,
    Hypernym,
    Hyponym,
    Meronym,
    Holonym,
    Troponym,
    CoordinateTerm,
    OtherwiseRelated
]

Collocation = Synonym.copy(
    name="collocations",
    template_names=["collocation", "coi","co"],
)



SEMANTIC_TEMPLATES = [
    Qualifier,
    Label,
    Gloss,
    Sense,
    *NYMS
]
