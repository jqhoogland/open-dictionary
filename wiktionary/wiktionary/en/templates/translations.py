from wiktionary.en.templates.base import _LANG, COMMON_RENAME, TemplateMapping

Translation = TemplateMapping(
    name="translation",
    template_names=["translation", "t", "t-check", "t+", "t+check", "tt", "tt+", "tt+check", "tt-check"],
    rename={
        "1": _LANG[1],
        "2": "gloss",
        # TODO: Add support for gender & number specification (|3=, |4=, ...)
        **COMMON_RENAME
    }
)

NoEquivalentTranslation = Translation.copy(
    template_names=["no equivalent translation"],
    extra={"subtype": "no_equivalent_translation"}
)


NotUsed = Translation.copy(
    template_names=["not used"],
    extra={"subtype": "not_used"}
)


TRANSLATION_TEMPLATES = [
    Translation,
    NoEquivalentTranslation,
    NotUsed
]
