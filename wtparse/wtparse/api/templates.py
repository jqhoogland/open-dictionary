from dataclasses import dataclass, field
from inspect import ArgSpec
from pprint import pp
import re
from typing import Literal, Protocol
import warnings
from more_itertools import first_true
import wikitextparser as wtp

from wtparse.wtypes import LanguageCode



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



Link = TemplateMapping(
    name="link",
    template_names=["l", "link"],
    rename={
        "1": "lang", "2": "page", "3": "alt", "4": "gloss",
        "t": "gloss", "sc": "script_code", "tr": "transliteration", "ts": "transcription", "pos": "part_of_speech", "lit": "literal_translation", "id": "sense_id"
    },
    ignore=("accel-form", "accel-translit", "accel-lemma", "accel-lemma-translit", "accel-gender", "accel-nostore")
)

DerivedTemplate = TemplateMapping(
    name="derived",
    template_names=["derived", "der"],
    rename={
        "alt": "alt_display", 
        "1": "lang", "2": "page", "3": "alt", "4": "gloss",
    },
)

Qualifier = TemplateMapping(
    name="qualifier",
    template_names=["qualifier", "q", "i", "qual"],
    rename={
        "1": "lang", "2": "word", "3": "gloss"
    }
)

template_mappers = (
    Link,
    Qualifier, 
    DerivedTemplate
)


def parse_template(template: wtp.Template) -> dict | None:
    template_mapper = first_true(
        template_mappers, 
        lambda tm: template.name in tm.template_names,
        None
    )

    if not template_mapper:
        return None

    data={}

    for i, arg in enumerate(template.arguments):
        if arg.name not in template_mapper.ignore:
            key = template_mapper.rename.get(arg.name, arg.name)
            data[key] = arg.value

    return {
        "name": template_mapper.name,
        **data
    }


def parse_templates(templates_raw: str) -> list[dict]:
    templates = wtp.parse(templates_raw).templates
    return [pt for t in templates if (pt := parse_template(t))]
