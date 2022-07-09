import json
from dataclasses import asdict
from typing import Literal

import typer
from pyld import jsonld

from wiktionary.api import WiktionaryClient
from wiktionary.en.parser import EnParser

Format =  Literal["json", "jsonld"]

def main(word: str, lang: str, wiki: str = "en", form: str = "json"):
    if wiki != "en":
        raise NotImplementedError("Non-English wiktionaries are not supported yet.")

    client = WiktionaryClient(parser=EnParser())

    if form == "json":
        entries = client.fetch_entry(word, lang)
        entries_json = json.dumps(
            [asdict(e) for e in entries], 
            indent=2,ensure_ascii=False
        ) 
    elif form == "jsonld":
        entries = client.fetch_jsonld(word, lang)
        # context = entries.pop("@context")
        # entries = jsonld.expand(entries, context)
        entries_json = json.dumps(entries,  indent=2,ensure_ascii=False)
    else: 
        raise ValueError(f"Unknown format: {form}")

    print(entries_json)

    return entries


if __name__ == "__main__":
    typer.run(main)
