import wikitextparser as wtp
from more_itertools import first_true
from wiktionary.en.templates.etymology import ETYMOLOGY_TEMPLATES
from wiktionary.en.templates.links import LINK_TEMPLATES
from wiktionary.en.templates.pronunciation import PRONUNCIATION_TEMPLATES
from wiktionary.en.templates.semantics import SEMANTIC_TEMPLATES

TEMPLATES = (
    *LINK_TEMPLATES,
    *ETYMOLOGY_TEMPLATES,
    *PRONUNCIATION_TEMPLATES,
    *SEMANTIC_TEMPLATES
)


def parse_template(template: wtp.Template) -> dict | None:
    mapper = first_true(
        TEMPLATES, 
        pred=lambda tm: template.name in tm.template_names,
        default=None
    ) 

    if not mapper:
        return None

    return mapper.transform(template)


def parse_templates(templates_raw: str) -> list[dict]:
    templates = wtp.parse(templates_raw).templates
    return [pt for t in templates if (pt := parse_template(t))]
