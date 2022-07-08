
from wiktionary.en.templates.base import TemplateMapping

Dialect = TemplateMapping(
    name="dialect",
    template_names=("accent", "a"),
    variadic_name="dialects",
    variadic_start="1",
    variadic_rename={"": "dialect"},
    extra_transform={"dialects": lambda ds: [d["dialect"] for d in ds]}
)

IPA = TemplateMapping(
    name="ipa",
    template_names=["IPA", ]
)


Audio = TemplateMapping(
    name="audio",
    template_names=["audio", ]
)

Rhymes= TemplateMapping(
    name="rhymes",
    template_names=["rhymes", ]
)

Homophone = TemplateMapping(
    name="homophone",
    template_names=["homophone", ]
)


PRONUNCIATION_TEMPLATES = [
    Dialect,
    IPA,
    Audio,
    Rhymes,
    Homophone,
]
