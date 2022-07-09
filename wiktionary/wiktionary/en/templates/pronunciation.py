
from wiktionary.en.templates.base import _LANG, COMMON_RENAME, TemplateMapping

Dialect = TemplateMapping(
    name="dialect",
    template_names=("accent", "a"),
    variadic_name="dialects",
    variadic_start="1",
    variadic_rename={"": "d"},
    extra_transform={"dialects": lambda ds: [d["d"] for d in ds]}
)

IPA = TemplateMapping(
    name="ipa",
    template_names=["IPA"],
    rename={
        "1": _LANG[1],
    },
    variadic_start="2",
    variadic_name="pronunciations",
    variadic_rename={"": "ipa", "qual": "qualifier", "ref": "ref"},
    ignore=("sort", "nocount")
)


Audio = TemplateMapping(
    name="audio",
    template_names=["audio", ],
    rename={
        "1": _LANG[1],
        "2": "filename",
        "3": "url",
        "format": "format",
    }
)

AudioWitihIPA = TemplateMapping(
    name="audio",
    template_names=["audio-IPA", ],
    rename={
        "1": _LANG[1],
        "2": "filename",
        "3": "ipa",
        "format": "format",
        "dial": "dialect"
    }
)

Rhymes= TemplateMapping(
    name="rhymes",
    template_names=["rhymes", ],
    rename={
        "1": _LANG[1],
    },
    variadic_name="rhymes",
    variadic_start="2",
    variadic_rename={"": "rhyme", "q": "qualifier", "s": "syllables"},
)

Homophone = TemplateMapping(
    name="homophones",
    template_names=["homophones", "homophone", "hmp" ],
    rename={
        "1": _LANG[1],
    },
    variadic_name="rhymes",
    variadic_start="2",
    variadic_rename={"": "homophone", "q": "qualifier", **COMMON_RENAME},
)

Hyphenation = TemplateMapping(
    name="hyphenation",
    template_names=["hyphenation", "hyph"],
    rename={
        "1": _LANG[1],
        "caption": "caption"
    },
    variadic_name="syllables",
    variadic_start="2",
    variadic_rename={"": "s"},
    extra_transform={"syllables": lambda ss: [s["s"] for s in ss]},
    ignore=("nocaption")
)


PRONUNCIATION_TEMPLATES = [
    Dialect,
    IPA,
    Audio,
    Rhymes,
    Homophone,
]
