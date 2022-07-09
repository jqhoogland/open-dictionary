import re
from typing import TypedDict

import wikitextparser as wtp

from wiktionary._types import Language, LanguageCode
from wiktionary.constants import LANGUAGES_TO_NAMES


def get_full_lang(lang: LanguageCode) -> Language:
    """Returns a capitalized, English version of the language corresponding to `lang`"""
    return LANGUAGES_TO_NAMES[lang].capitalize() # type: ignore


def to_snake_case(word):
    """Converts a sentence to snake_case"""
    return word.lower().replace(" ", "_")
 

def get_regex(d: dict[str, str], key: str, default: str | None = None) -> str | None:
    """Find the first key that matches a regex expression, and return the value.    

    TODO: use regex substitution with the value    
    """
    for k, v in d.items():
        if re.match(k, key):
            return v
    return default


def template_to_dict(template: wtp.Template) -> dict:
    """Convert a wikitext template to a dictionary, without renaming any of the keys"""
    data = {
        arg.name: arg.value
        for arg in template.arguments
    }
    data["template"] = template.name.replace(" ", "_").lower()

    return data


class TransformValue(TypedDict, total=False):
    key: str
    value: str

def transform_template_dict(
    template: wtp.Template, 
    transforms: dict[str, str | dict[str, str | TransformValue]]
) -> dict:
    """Transforms a dictionarified template in order to, for example give positional arguments ("1", "2", etc.) sensible names, to expand overly terse keyword arguments, and to listify variadic arguments.    

    Expects a dictionary of `transforms`. 
    - The keys are the `@type` of the transformed templates.
    - If an argument is a `str`, it is an alias to another element in `transforms`.
        - E.g.` { "my_key": {...}, "my_alias": "my_key" }`
    - If an argument is a `dict`, it is a mapping from the argument name to a new name.
       - E.g. `{ "my_key": { "1": "some_new_name" } }` will map the first positional argument of the `template` named `my_key` to the key `some_new_name`.

    These mapping arguments can include regex & nested mappings.
    E.g.:
    ```
    {
        "g": "genders[0]",
        "g(\\d+)": "genders[$1]"
    }
    ```
    will map a template `{{my_template|g=f-s|g2=m-p|g3=f-p}}` to:
    ```
    {   
        "genders": ["f-s", "m-p", "f-p"]
    }
    ```
    and
    ```
    {
        "g": "genders[0].g",
        "g(\\d+)": "genders[$1].g"
    }
    ```
    will map a template `{{my_template|g=f-s|g2=m-p|g3=f-p}}` to:
    ```
    {   
        "genders": [{"g": "f-s"}, {"g": "m-p"}, {"g": "f-p"}]
    }
    ```

    """
    raise NotImplementedError("Just use the existing transformer. It's good enough for now.")

    template_type = template.pop("@template")
    transformation = transforms.get(template_type, None)

    if transformation is None:
        # If no transformation is specified, we leave the template as-is
        return {
            "@type": "wt:wiki/Template:" + template_type,
            **template
        }
    elif isinstance(transformation, str):
        # If the transformation is a string, we follow the alias
        template_type = transformation
        transformation = transforms[transformation]

        if not isinstance(transformation, dict):
            raise ValueError(
                f"Insuitable `transforms` provided. Found element {transformation}"
            )

    def _transform_template_dict(template: dict[str, str | TransformValue], transformation: dict[str, str]):
        data = {}
        for src_key, src_value in template.items():
            for trans_key, trans_value in transformation.items():
                if (m := re.match(trans_key, src_key)):
                    groups = m.groups()
                    # TODO
                
        return data

    return {
        "@type": template_type,
        **_transform_template_dict(template, transformation)
    }
