from wiktionary.en.templates.base import _LANG, TemplateMapping

Anagram = TemplateMapping(
    name="anagram",
    template_names=["anagrams", "anagram"],
    rename={
        "1": _LANG[1],
        "a": "alphagram"
    },
    variadic_name="anagrams",
    variadic_start="2",
    variadic_rename={"": "a"},
    extra_transform={"anagrams": lambda anagrams: [a["a"] for a in anagrams]},
)

OTHER_TEMPLATES = [
    Anagram
]
