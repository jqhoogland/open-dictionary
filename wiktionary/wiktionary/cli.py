import json
from dataclasses import asdict

import typer

from wiktionary.api import WiktionaryClient
from wiktionary.en.parser import EnParser


def main(word: str, lang: str, wiki: str = "en"):
    if wiki != "en":
        raise NotImplementedError("Non-English wiktionaries are not supported yet.")

    client = WiktionaryClient(parser=EnParser())

    entries = client.fetch_entry(word, lang)

    entries_json = json.dumps([asdict(e) for e in entries], indent=2)
    print(entries_json)

    return entries


if __name__ == "__main__":
    typer.run(main)
