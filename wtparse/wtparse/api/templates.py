from dataclasses import dataclass, field
from inspect import ArgSpec
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

    #: Arguments to ignore
    ignore: tuple[str] = ()

    def transform(self, template: wtp.Template):
        data = {}

        for i, arg in enumerate(template.arguments):
            if arg.name not in self.ignore:
                key = self.rename.get(arg.name, None) \
                    or get_regex(self.rename, arg.name, arg.name)

                data[key] = arg.value

        return {
            "name": self.name,
            **data
        }


# Links

shared_rename = {
    "t": "gloss", "sc": "script_code", "tr": "transliteration", "ts": "transcription", "pos": "part_of_speech", "lit": "literal_translation", "id": "sense_id"
}

Link = TemplateMapping(
    name="link",
    template_names=["l", "link", "l-self", "ll"],
    rename={
        "1": "lang", "2": "target", "3": "alt", "4": "gloss",
        **shared_rename
    },
    ignore=("accel-form", "accel-translit", "accel-lemma", "accel-lemma-translit", "accel-gender", "accel-nostore")
)

Mention = TemplateMapping(
    name="mention",
    template_names=["m", "mention", "m-self"],
    rename=Link.rename,
    ignore=Link.ignore
)

# Etymology

Derived = TemplateMapping(
    name="derived",
    template_names=["derived", "der"],
    rename={
        **shared_rename,
        "1": "target_lang", "2": "source_lang", "3": "source", "4": "alt",
        "5": "gloss", "nocat": "no_categorization", "sort": "sort_key"
    },
)

Borrowed = TemplateMapping(
    name="borrowed",
    template_names=["borrowed", "bor", "bor+"],
    rename={
        **Derived.rename,
        # Also: "conj" for joining multiple sources
    },
)

LearnedBorrowing = TemplateMapping(
    name="learned_borrowing",
    template_names=["learned borrowing", "lbor", "lbor+"],
    rename=Borrowed.rename,
    ignore=("nocap", "notext")
)

OrthographicBorrowing = TemplateMapping(
    name="orthographic_borrowing",
    template_names=["orthographic borrowing", "obor", "obor+"],
    rename=Borrowed.rename,
    ignore=("nocap", "notext")
)

class Root:
    """
    Status: Not Tested
    [Source](https://en.wiktionary.org/wiki/Template:root)
    """
    name="root"
    template_names=["root"]

    @classmethod
    def transform(cls, template: wtp.Template):
        args = iter(template.arguments)
        data = {
            "name": "root",
            "target_lang": next(args),
            "source_lang": next(args),
            "roots": []
        }
        
        # Build with a dict because we don't know if the order is correct
        roots = {}
        for arg in args:
            if re.match('^\d+$', arg.name):
                roots[arg.name] = roots[arg.name] or {}
                roots[arg.name].update({"root": arg.value})
            elif re.match('^id\d+$', arg.name):
                roots[arg.name[2:]] = roots[arg.name[2:]] or {}
                roots[arg.name[2:]].update({"sense_id": arg.value})

        for root in roots.values():
            data["roots"].append(root)
        
        return roots

# Other

class Qualifier:
    name="qualifier",
    template_names=["qualifier", "qual", "i", "q"],

    @classmethod
    def transform(cls, template: wtp.Template):
        return {
            "name": "qualifier",
            "qualifiers": [a.value for a in template.arguments]
        }


template_mappers = (
    # Links
    Link,
    Mention,
    
    # Etymology
    Borrowed,
    LearnedBorrowing,
    OrthographicBorrowing,
    Root,
    
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
