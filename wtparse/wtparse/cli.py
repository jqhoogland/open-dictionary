"""
### Frequency Lists
Raw frequency lists aren't very useful.
They're full of redundancies (e.g., "run", "runs", "ran" are all the same underlying word).
They also hide synonyms (e.g., "run" as verb vs. "run" as noun).

### What this file does:
Load a frequency list derived from [open subtitles](https://github.com/hermitdave/FrequencyWords),
lemmatize the words, split by definitions, and reorder.
"""
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
from wtparse.core import fetch_entry

# typer doesn't accept literal values
def main(language: str, word: str):
    pp(fetch_entry(word, language))


if __name__ == "__main__":
    typer.run(main)
