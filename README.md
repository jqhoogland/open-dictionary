# Open Dictionary

📖 [Open Dictionary](https://open-dictionary.vercel.app/) is structured, machine-readible [Wiktionary](https://www.wiktionary.org/). 

# 🚀 Start here

- Check out the [REST API](https://open-dictionary.vercel.app/docs/rest/v1.html),
- Or the GraphQL API.
- Try the Typescript Client,
- Or the Python Client.

Sorry, I lied — it's not actually ready yet. So stay tuned (or contribute if you really can't wait).

---

# ☠️ The Problem
Wiktionary has no API. 

If you want your query Wiktionary, you have to use a parser like [this one](https://github.com/Suyash458/WiktionaryParser). Unforunately, existing parsers are non-exhaustive (many fields and relationships are thrown out), insufficiently structured (Wiktionary articles are blobs of wiki-flavored markdown), and limited in scope (layout standards vary between language-specific Wiktionaries).

# 🗺 What to expect
We're manually building crawlers and parsers for each language-specific Wiktionary to capture/save the data and make it easier to use.

- That means (eventually) easily consumable APIs. — REST, GraphQL, plus clients for `insert-your-favorite-programming-language-here`
- Better tools for NLP — built in semantic web visualization, lemmatizers & tokenizers, etc. 
- Better tools for language-learning — finding translations, pronunciations, and word frequency lists.

# ❓ How it works
The internal data model is based on the ["triples"](https://en.wikipedia.org/wiki/Semantic_triple) of the [semantic web](https://en.wikipedia.org/wiki/Semantic_Web). In that sense it's similar to [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) with some language-specific details. 

Relations between words [that are currently represented by headings](https://en.wiktionary.org/wiki/Wiktionary:Entry_layout) are represented by triples of `subject`, `predicate` (e.g., "synonym", "antonym", "translation", "lexeme"), and `object`. This means relations that are extensible but consistent.

---

This is an app bootstrapped according to the [init.tips](https://init.tips) stack, also known as the T3-Stack.
