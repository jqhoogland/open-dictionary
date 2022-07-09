# Open Dictionary Ontology

This provides a [semantic web ontology](https://www.w3.org/standards/semanticweb/ontology) for the relationships between words in natural languages. 

The aim is a standard representation that can serve as a "compile" target of different wiktionaries' entries. This way, we'll be able to convert entries from `en.wiktionary.org`, `fr.wiktionary.org`, etc. to a consistent data structure. 

By using the conventions of the semantic web, we can use take advantage of existing tooling (like [SPARQL](https://en.wikipedia.org/wiki/SPARQL)). 

It's expressed in terms of [JSON-LD](https://www.w3.org/TR/json-ld/) rather than [RDF](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/Overview.html) because it'll be more familiar to those who are new to the semantic web.
 
# The semantic web

The "semantic" web starts with a simple idea. Instead of links that just point from one web page to another, the semantic web introduces the idea of "labeled" links, so we can specify what kind of link we have.

This idea forms the basis of semantic web "[triples](https://en.wikipedia.org/wiki/Semantic_triple)", which are trios of a "subject", "predicate", and "object". These are basic sentences like "John is 30 years old", or "cars are vehicles". 

With the additional requirement that subjects, predicates, and objects are labeled by unique URIs, triples can be unambiguously queried by machines ([example](https://en.wikipedia.org/wiki/Semantic_triple#Subject,_predicate_and_object)).

"[Ontologies](https://en.wikipedia.org/wiki/Ontology_(information_science))" or "vocabularies" are systematic naming conventions for particular domains. In the semantic web, an "[ontology](https://www.w3.org/standards/semanticweb/ontology" refers to a collection of URIs (actually [IRIs](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier)) that people can "import" into their triple definitions. 

Some of these are very general, like [OWL](https://www.w3.org/TR/owl-features/), which provides building pieces for defining properties & classes. Others, like [FOAF](https://en.wikipedia.org/wiki/FOAF_(ontology)) provides definitions for defining relationships between people.

This ontology is a collection of definitions for concepts in natural language like "is a synonym of", "is a translation of", or "has the transliteration". There may already exist an ontology for this purpose, but I couldn't find one (so please point me to an existing standard if you know of one).

[Read more about the semantic web here.](https://en.wikipedia.org/wiki/Semantic_Web#Components)

# Ok, but the semantic web is dead

So it's true that most of the semantic web stuff happened more than a decade ago and has been pretty much forgotten. This was the original "Web3" before we got today's "Web3". (Also, most of it is based on XML 🤢).

Of the two, I'm still betting on the first "Web3". Not just because [Tim Berners Lee is still fighting for it with tooth and nail](https://solidproject.org/). No, it's just a really good idea that deserves more attention. And it offers valuable insights even in the absence of a large community of true practitioners.

# [JSON-LD](https://www.w3.org/TR/json-ld/)

A few important notes:
- JSON-LD arrays are unordered by default, and must be labeled explicitly with `@list`