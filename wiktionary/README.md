# Wiktionary API 

This is a **non-official** Wiktionary API client written in Python. 

## The Problem

There is an actual [Wiktionary API](https://en.wiktionary.org/w/api.php).

Unfortunately, it only returns pages in `html` or `wikitext` (Wikipedia's internal markup language) — not the friendliest for computers to read. 
Fortunately, `wikitext` has a decent bit of internal structure and is ~~easy~~ not impossible to work with.

This library provides a client that uses [wikitextparser](https://github.com/5j9/wikitextparser) (plus some custom logic) to convert wikitext into 
straightforward `json` objects (read: Python dictionaries) that you can use at your leisure.

It's much more comprehensive and accurate than [WiktionaryParser](https://github.com/Suyash458/WiktionaryParser) since it works with the raw wikitext rather than the generated html.

## One Wiktionary to rule them all.

There's one problem: Wiktionary is not one thing. 

No [there are 183 different Wiktionaries in 183 different languages](https://meta.wikimedia.org/wiki/Wiktionary#List_of_Wiktionaries). 
Pretty much every single Wiktionary has its own, non-interoperable standards. So you have to have to build unique parsing logic for each Wiktionary.

(These are identified by the an [ISO 639 code](https://www.iso.org/iso-639-language-codes.html) subdomain (as in `en.wiktionary.com`))

So... we're starting with the English-language Wiktionary. Depending on how that goes, we might move on to additional wiktionaries.



