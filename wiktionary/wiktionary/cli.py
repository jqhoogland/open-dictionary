from pprint import pp

import typer

from wiktionary.api import WiktionaryClient
from wiktionary.en.parser import EnParser


def main(word: str, lang: str, wiki: str = "en"):
    if wiki != "en":
        raise NotImplementedError("Non-English wiktionaries are not supported yet.")

    client = WiktionaryClient(parser=EnParser())

    entry = client.fetch_entry(word, lang)
    pp(entry)

    return entry


if __name__ == "__main__":
    typer.run(main)
