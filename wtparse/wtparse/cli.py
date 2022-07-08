from pprint import pp

import typer

from wtparse.api import Entry


# typer doesn't accept literal values
def main(wiki: str, word: str):
    pp(Entry.from_wiktionary(word, wiki))


if __name__ == "__main__":
    typer.run(main)
