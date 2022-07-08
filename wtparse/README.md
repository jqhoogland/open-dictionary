# Wiktionary Parse (`wtparse`)

Unfortunately, the [Wiktionary API](https://en.wiktionary.org/w/api.php) only returns pages in `html` or `wikitext` (Wikipedia's internal markup language). 
Fortunately, `wikitext` has a decent bit of internal structure and is ~~easy~~ not impossible to work with.

This library provides a Python API client for the Wiktionary
API that uses [wikitextparser](https://github.com/5j9/wikitextparser) to convert wikitext into 
straightforward `json` objects (read: Python dictionaries).

It's more comprehensive and extensible than [WiktionaryParser](https://github.com/Suyash458/WiktionaryParser), which
parses the lower fidelity outputted `html`. 


