import re
import warnings
from dataclasses import dataclass, field
from inspect import ArgSpec
from pipes import Template
from typing import Callable, Literal, Protocol, TypeVar

import wikitextparser as wtp
from more_itertools import first_true
from wiktionary._types import LanguageCode
from wiktionary.utils import get_regex

_LANG = "lang", "lang"
_ALT = "alt", "alt"
_T = "t", "gloss"
_SC = "sc", "script"
_TR = "tr", "transliteration"
_TS = "ts", "transcription"
_POS  = "pos", "partOfSpeech"
_LIT = "lit", "literalTranslation"
_ID = "id", "sense"

_G = "g", "gender"
WITH_GENDER = dict(
    variadic_name="genders",
    variadic_rename={"g": "g"},
    extra_transform={"genders": lambda gs: [g["g"] for g in gs]}
)

COMMON_IGNORE = 'accel', 'nocap', 'notext', 'nocat', 'sort', "accel-form", "accel-translit", "accel-lemma", "accel-lemma-translit", "accel-gender", "accel-nostore" 

COMMON_RENAME = dict((
    _LANG,
    _ALT,
    _T,
    _SC,
    _TR,
    _TS,
    _POS,
    _LIT,
    _ID
))

COMPOUND_TYPES = {
    "allit": "alliterative",
    "ant": "antonymous",
    "bahu": "bahuvrihi",
    "bv": "bahuvrihi",
    "coord": "coordinative",
    "desc": "descriptive",
    "det": "determinative",
    "dva": "dvandva",
    "endo": "endocentric",
    "exo": "exocentric",
    "karma": "karmadharaya",
    "kd": "karmadharaya",
    "rhy": "rhyming",
    "syn": "synonymous",
    "tat": "tatpurusa",
    "tp": "tatpurusa",
}

ABBREVIATED_POS = {
    "adj": "Adjective",
    "adv": "Adverb",
    "con": "Conjunction",
    "det": "Determiner",
    "interj": "Interjection",
    "noun": "Noun",
    "num": "Numeral",
    "part": "Particle",
    "postp": "Postposition",
    "prep": "Preposition",
    "pron": "Pronoun",
    "proper noun": "Proper noun",
    "verb": "Verb",
}


# TODO: Some magic with metaclasses so that the template mappings
#       are their own classes rather than implementations of TemplateMapping.
@dataclass
class TemplateMapping:
    """
    [Templates](https://en.wiktionary.org/wiki/Wiktionary:Templates) are a feature of wikitext for duplicating formatting structured content across pages.

    A wiktionary template looks something like:
    
    `{{name|arg_0|arg_1|key_0=arg_2|key_1=arg_3}}`

    A template is identified by two curly braces `{{...}}` with arguments separated by `|`. The first argument is the name of the template. Subsequent arguments are either positional or `key=value` pairs.    
    
    One template can have have multiple names/aliases (such as `member`/`m`).
    One argument can be both positional and key=value.

    We want to map templates to a dictionary, for example `{{m|en|hello|t=a standard greeting}}}}` becomes:

    ```json
    {   
        "@id": "mention",
        "word": "hello",
        "lang": "en",
        "gloss": "a standard greeting"        
    }
    ```

    TODO: Figure out the gender/number/animacy labels (which have somewhat dynamic keys)

    """

    #: The value we give to `name` in the produced dictionary.
    name: str
    
    #: The names of the template to match against, e.g. `["m", "mention"]`.
    template_names: list[str] 

    #: Mapping from template arg names to the keys in the outputted dictionary.
    #: If not listed here (nor under `ignore`), use the existing name.
    #: Positional args are named "1", "2", ... (not my fault, blame wiktionary).
    rename: dict[str, str] = field(default_factory=dict)

    #: Some templates are variadic. For example, `{{affix|nl|huis|-je|pos2=diminutive}}`. We'd like to convert this into 
    #: ```
    #: {
    #:   "@id": "affix", 
    #:   "lang": "nl", 
    #:   "morphemes": [
    #:     {"morpheme": "huis"}, 
    #:     {"morpheme": "-je", "part_of_speech": "diminutive"}
    #:   ]
    #: }
    #: `variadic_name`: the name of the list of variadic arguments.
    #: `variadic_start` is the *string* index of the first variadic argument, then 
    #: `variadic_rename` is the same as `rename` but arguments are assumed to end #: in a number.
    #: If any of the values of `variadic_rename` are empty (`=""`), store the value directly (rather than in a subdictionary)
    variadic_name: str = "values"
    variadic_start: str | None = field(default=None)
    variadic_rename: dict = field(default_factory=dict)

    #: Dictionary of transformations to apply to the final dictionaries
    extra_transform: dict = field(default_factory=dict)

    #: Extra information to attach to the produced dictionary.
    extra: dict  = field(default_factory=dict)

    #: Arguments to ignore
    ignore: tuple[str] = COMMON_IGNORE

    def variadic_transform(self, data: dict) -> None:
        if self.variadic_start is None:
            return

        start = int(self.variadic_start)
        idx = start
        variadic_args = {}

        # Get positional arguments ("3", "4",...)
        while (item := data.pop(str(idx), None)) is not None:
            key = self.variadic_rename.get("", "value")
            variadic_args[idx-start] = {key: item}
            idx += 1

        # Get prefixed arguments ("id1", "id2")
        # Note kwarg "id1" does not necessarily match pos arg "1"
        for k in [*data.keys()]:
            if (m := re.match(r"^(\w+)(\d+)$", k)):
                v = data.pop(k)
                k, idx = m.groups()

                k = self.variadic_rename.get(k, k)
                idx = int(idx) -1 

                if k in self.extra_transform:
                    v = self.extra_transform[k](v)

                variadic_args[idx] = variadic_args[idx] or {}
                variadic_args[idx][k] = v

        variadic_list = [variadic_args[k] for k in sorted(variadic_args.keys())]
        data[self.variadic_name] = variadic_list

    def transform(self, template: wtp.Template):
        data = {}

        # Transform non-variadic arguments
        for arg in template.arguments:
            if arg.name not in self.ignore:
                k = self.rename.get(arg.name, arg.name)
                v = arg.value
                data[k] = v

        # Transform variadic arguments
        self.variadic_transform(data)

        # Apply final transformations
        for k in self.extra_transform:
            if k in data:
                data[k] = self.extra_transform[k](data[k])

        data.update({**self.extra})

        return {
            "@id": self.name,
            **data
        }

    def copy(self, **kwargs):
        data = {**self.__dict__}
        data.update(kwargs)
        return self.__class__(**data)


