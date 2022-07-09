# Open Dictionary

📖 [Open Dictionary](https://open-dictionary.vercel.app/) is structured, machine-readable [Wiktionary](https://www.wiktionary.org/). 

## 🚀 Start here

- Check out the [Python Client](/wiktionary).

Come back soon to check out:
- A REST API
- Or GraphQL API.
- And Typescript Client.

With these, you'll find:
- Better tools for NLP — built-in semantic web visualization, lemmatizers & tokenizers, etc. 
- Better tools for language-learning — finding translations, pronunciations, and word frequency lists.

## ☠️ The Problem
Wiktionary has no API.[^1] 

[^1]: It [actually has an api](https://en.wiktionary.org/w/api.php), but the api returns an unworkable sludge of html or [wikitext](https://en.wikipedia.org/wiki/Help:Wikitext).

Until now, querying Wiktionary programmatically required a parser like [this one](https://github.com/Suyash458/WiktionaryParser). 
This is not ideal since these parsers work with outputted html rather than the raw [wikitext](https://en.wikipedia.org/wiki/Help:Wikitext) used to generate the pages.

There's also the problem that Wiktionaries vary in standards across languages, so existing parsers are Wiktionary-specific. That means they throw out a lot of otherwise useful data. 

## 🏗 The Solution

We provide tools to convert [wikitext](https://en.wikipedia.org/wiki/Help:Wikitext) into queryable ["semantic triples"](https://en.wikipedia.org/wiki/Semantic_triple),
and we expose these via easy-to-use APIs.

On top of that, we (will eventually) offer a few other niceties like tools to visualize the graph of words, lemmatize inflected forms, etc.

These triples serve as a kind of language-agnostic compile target for different wiktionaries, which means we can eventually consolidate all wiktionaries into one consistent format. 
For more, check out the [wiktionary parser](./wiktionary).

(The tools translate readily to Wikipedia, so feel free to intiative with that follow-up.) 
