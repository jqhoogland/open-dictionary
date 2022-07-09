
from wiktionary.en.templates.base import (_ALT, _G, _LANG, _T, COMMON_IGNORE,
                                          COMMON_RENAME, COMPOUND_TYPES,
                                          WITH_GENDER, TemplateMapping)

Derived = TemplateMapping(
    name="derived",
    template_names=["derived", "der"],
    rename={
        **COMMON_RENAME,
        "1": _LANG[1], "2": "srcLang", "3": "src", "4": _ALT[1],
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
    rename={"1": "dstLang", "2": "srcLang"},
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
        "1": _LANG[1], "type": "compoundType", **COMMON_RENAME
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
        "1": _LANG[1], "2": "srcLang", "3": _ALT[1], "4": _T[1], 
        **COMMON_RENAME
    },
    **WITH_GENDER
)


ShortFor = TemplateMapping(
    name="shortFor",
    template_names=["short for", "clipping"],
    rename={
        "1": _LANG[1], "2": "word", "3": _ALT[1], "4": _T[1], 
        **COMMON_RENAME
    },
    **WITH_GENDER,
    ignore=(*COMMON_IGNORE, "nodot", "dot")
)

BackFormation = TemplateMapping(
    name="backFormation",
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
        "1": _LANG[1], "2": "srcLang", "3": "src", "4": _ALT[1], "5": _T[1],
        **COMMON_RENAME
    },
    **WITH_GENDER
)

SemanticLoan = Calque.copy(
    template_names=["semantic loan", "sl"],
    extra={"subtype": "SemanticLoan"}
)

PhonoSemanticMatching = Calque.copy(
    template_names=["phono-semantic matching", 'psm'],
    extra={"subtype": "PhonoSemanticMatching"}
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
    template_names=["rfe", "etystub"],
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

ETYMOLOGY_TEMPLATES = (
    # Etymology
    Derived,
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
)

