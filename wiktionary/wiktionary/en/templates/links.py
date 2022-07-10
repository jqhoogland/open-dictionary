
from wiktionary.en.templates.base import (_ALT, _LANG, _T, COMMON_RENAME,
                                    WITH_GENDER, TemplateMapping)

Link = TemplateMapping(
    name="link",
    template_names=["l", "link", "l-self", "ll"],
    rename={
        "1": _LANG[1], "2": "src", "3": _ALT[1], "4": _T[1],
        **COMMON_RENAME
    },
    **WITH_GENDER
)

Mention = TemplateMapping(
    name="mention",
    template_names=["m", "mention", "m-self", "langname-mention"],
    rename=Link.rename,
    ignore=Link.ignore
)

LINK_TEMPLATES = (
    Link,
    Mention,
)
