import json
from pprint import pp

from tqdm import tqdm

import typer

from wtparse.constants import LANGUAGES
from wtparse.wtypes import (
    Word,
    LanguageCode,
    PartOfSpeech,
)
from wtparse.api import get_entry

# typer doesn't accept literal values
def main(wiki: str, word: str):
    pp(get_entry(word, wiki))


if __name__ == "__main__":
    typer.run(main)
