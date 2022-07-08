from dataclasses import dataclass, field
from inspect import ArgSpec
from pipes import Template
from pprint import pp
import re
from typing import Callable, Literal, Protocol, TypeVar
import warnings
from more_itertools import first_true
import wikitextparser as wtp
from wtparse.utils import get_regex

from wtparse.wtypes import LanguageCode


def get_arg(template: wtp.Template, arg_name: str) -> wtp.Argument | None:
    return first_true(template.arguments, pred=lambda a: a.name == arg_name )

_LANG = "lang", "lang"
_ALT = "alt", "alt"
_T = "t", "gloss"
_SC = "sc", "script_code"
_TR = "tr", "transliteration"
_TS = "ts", "transcription"
_POS  = "pos", "part_of_speech"
_LIT = "lit", "literal_translation"
_ID = "id", "sense_id"

_G = "g", "gender"
WITH_GENDER = dict(
    variadic_name="genders",
    variadic_rename={"g": _G[1]},
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
        "type": "mention",
        "word": "hello",
        "lang": "en",
        "gloss": "a standard greeting"        
    }
    ```

    TODO: Figure out the gender/number/animacy labels (which have somewhat dynamic keys)

    """

    #: The value we give to `type` in the produced dictionary.
    name: str
    
    #: The names of the template to match against, e.g. `["m", "member"]`.
    template_names: list[str] 

    #: Mapping from template arg names to the keys in the outputted dictionary.
    #: If not listed here (nor under `ignore`), use the existing name.
    #: Positional args are named "1", "2", ... (not my fault, blame wiktionary).
    rename: dict[str, str] = field(default_factory=dict)

    #: Some templates are variadic. For example, `{{affix|nl|huis|-je|pos2=diminutive}}`. We'd like to convert this into 
    #: ```
    #: {
    #:   "name": "affix", 
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

                if k == "":
                    variadic_args[idx] = v
                else:
                    variadic_args[idx] = variadic_args[idx] or {}
                    variadic_args[idx][k] = v

        variadic_list = [variadic_args[k] for k in sorted(variadic_args.keys())]
        data[self.variadic_name] = variadic_list

    def transform(self, template: wtp.Template):
        data = {}

        for arg in template.arguments:
            if arg.name not in self.ignore:
                k = self.rename.get(arg.name, arg.name)
                v = arg.value

                if k in self.extra_transform:
                    v = self.extra_transform[k](v)

                data[k] = v

        self.variadic_transform(data)
        data.update({**self.extra})

        return {
            "name": self.name,
            **data
        }

    def copy(self, **kwargs):
        data = {**self.__dict__}
        data.update(kwargs)
        return self.__class__(**data)


# Links


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

# Etymology

Derived = TemplateMapping(
    name="derived",
    template_names=["derived", "der"],
    rename={
        **COMMON_RENAME,
        "1": _LANG[1], "2": "src_lang", "3": "src", "4": _ALT[1],
        "5": _T[1]
    },
)

Borrowed = Derived.copy(
    name="borrowed",
    template_names=["borrowed", "bor", "bor+"],
)

LearnedBorrowing = Borrowed.copy(
    name="learned_borrowing",
    template_names=["learned borrowing", "lbor", "lbor+"],
)

OrthographicBorrowing = Borrowed.copy(
    name="orthographic_borrowing",
    template_names=["orthographic borrowing", "obor", "obor+"],
)

Root = TemplateMapping(
    name="root",
    template_names=["root"],
    rename={"1": "target_lang", "2": "src_lang"},
    variadic_start='3',
    variadic_rename={**COMMON_RENAME},
)

# Agglutination

# TODO: Add support for hyphens -> category 
# https://en.wiktionary.org/wiki/Template:affix
Compound = TemplateMapping(
    name="compound",
    template_names=["compound", "com"],
    rename={
        "1": _LANG[1], "type": "compound_type", **COMMON_RENAME
    },
    variadic_name="morphemes",
    variadic_start="2",
    variadic_rename={**COMMON_RENAME, "g": _G[1]},
    extra_transform={
        "compound_type": lambda t: COMPOUND_TYPES.get(t, t)
    },
)

Affix = Compound.copy(
    template_names=["affix", "af"],
    extra={
        "subtype": "affix"
    }
)

Blend = Compound.copy(
    template_names=["blend"],
    extra={
        "subtype": "blend"
    }
)

Prefix = Compound.copy(
    template_names=["prefix", "pre", "suffix"],
    extra={"subtype": "prefix"}
)

Confix = Compound.copy(
    template_names=["confix", "con"], 
    extra={"subtype": "confix"}
)


Suffix = Compound.copy(
    template_names=["suffix"], #, "suf"],
    extra={"subtype": "suffix"}
)

Interfix = Compound.copy(
    template_names=["interfix", "inter"],
    extra={"subtype": "interfix"}
)


# Shortenings

Clipping = TemplateMapping(
    name="clipping",
    template_names=["clipping of", "clipping"],
    rename={
        "1": _LANG[1], "2": "src_lang", "3": _ALT[1], "4": _T[1], 
        **COMMON_RENAME
    },
    **WITH_GENDER
)


ShortFor = TemplateMapping(
    name="short_for",
    template_names=["short for", "clipping"],
    rename={
        "1": _LANG[1], "2": "word", "3": _ALT[1], "4": _T[1], 
        **COMMON_RENAME
    },
    **WITH_GENDER,
    ignore=(*COMMON_IGNORE, "nodot", "dot")
)

BackFormation = TemplateMapping(
    name="back_formation",
    template_names=["back-formation", "back-form", "bf"],
    rename={
        "1": _LANG[1], "2": "word", "3": _ALT[1], "4": _T[1], 
        **COMMON_RENAME
    },
    **WITH_GENDER,
)


Doublet = TemplateMapping(
    name="doublet",
    template_names=["doublet", "dbt"],
    rename={
        "1": _LANG[1],
    },
    variadic_name="doublets",
    variadic_start="2",
    variadic_rename={**COMMON_RENAME, "g": _G[1]},
)

PiecewiseDoublet = Doublet.copy(
    template_names=["piecewise doublet"],
    extra={"subtype": "piecewise"},
)

Onomatopoeic = TemplateMapping(
    name="onomatopoeic",
    template_names=["onomatopoeic", "onom"],
    rename={
        "1": _LANG[1], "title": _ALT[1]
    }
)

Calque = TemplateMapping(
    name="calque",
    template_names=["calque", "cal", "clq"],
    rename={
        "1": _LANG[1], "2": "src_lang", "3": "src", "4": _ALT[1], "5": _T[1],
        **COMMON_RENAME
    },
    **WITH_GENDER
)

SemanticLoan = Calque.copy(
    template_names=["semantic loan", "sl"],
    extra={"subtype": "semantic_loan"}
)

PhonoSemanticMatching = Calque.copy(
    template_names=["phono-semantic matching", 'psm'],
    extra={"subtype": "phono-semantic matching"}
)

Eponym = TemplateMapping(
    name="eponym",
    template_names=["named-after"],
    rename={
        "1": _LANG[1], "2": "person", "nat": "nationality", "occ": "occupation", "wplink": "wplink", "born": "born", "died": "died",
        **COMMON_RENAME 
    }
)

Cognate = TemplateMapping(
    name="cognate",
    template_names=["cognate", "cog"],
    rename={
        **COMMON_RENAME,
        "1": _LANG[1], "2": "word", "3": _ALT[1],
        "4": _T[1]
    },
    **WITH_GENDER
)

Noncognate = Cognate.copy(
    name="noncognate",
    template_names=["noncognate", "noncog", "ncog", "nc"],
)

RequestForEtymology = TemplateMapping(
    name="rfe",
    template_names=["rfe"],
    rename={
        "1": _LANG[1], "2": "comment",
    },
    ignore=(*COMMON_IGNORE, "y", "m", "fragment", "section", "box", "noes")
)

Unknown = TemplateMapping(
    name="unknown",
    template_names=["unknown", "unk"],
    rename={
        "1": _LANG[1], "title": "alt",
    },
)



# Other

Qualifier = TemplateMapping(
    name="qualifier",
    template_names=["qualifier", "qual", "i", "q"],
    variadic_name="qualifiers",
    variadic_start='1',
    variadic_rename={"": "qualifier"},
)


template_mappers = (
    # Links
    Link,
    Mention,
    
    # Etymology
    Borrowed,
    LearnedBorrowing,
    OrthographicBorrowing,
    Root,
    Compound,
    Prefix,
    Confix,
    Suffix,
    Affix,
    Blend,
    Clipping,
    ShortFor,
    BackFormation,
    Doublet,
    PiecewiseDoublet, 
    Onomatopoeic, 
    Calque,
    SemanticLoan, 
    PhonoSemanticMatching,
    Eponym,
    Cognate,
    Noncognate,
    RequestForEtymology,
    Unknown,

    # Other
    Qualifier, 
    Derived,


)


def parse_template(template: wtp.Template) -> dict | None:
    mapper = first_true(
        template_mappers, 
        pred=lambda tm: template.name in tm.template_names,
        default=None
    ) 

    if not mapper:
        return None

    return mapper.transform(template)


def parse_templates(templates_raw: str) -> list[dict]:
    templates = wtp.parse(templates_raw).templates
    return [pt for t in templates if (pt := parse_template(t))]
