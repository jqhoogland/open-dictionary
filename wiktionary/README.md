# Wiktionary API 

> This is a **non-official** Wiktionary API client written in Python. 
>
> This is very non-stable. Expect many breaking changes.

## ❓ How it works

Wiktionary articles contain lots of internal structure in the form of [templates](https://meta.wikimedia.org/wiki/Help:Template).
With a bit of manual pruning, we convert these templates into Wiktionary-agnostic ["semantic triples"](https://en.wikipedia.org/wiki/SemanticTriple). (These use a new [ontology for natural language](/ontology)).

(Note: they're not perfect triples yet.)

Then, with [SPARQL](https://en.wikipedia.org/wiki/SPARQL) and tools built on top of it ([GraphQL-LD](https://github.com/rubensworks/GraphQL-LD.js)),
we can query the data consistently.

In actual fact, there's a bit more going on: we look at context (so section headings & also crawl standard wikilinks and non-templated information).

## The Problem

There is an actual [Wiktionary API](https://en.wiktionary.org/w/api.php).

Unfortunately, it only returns pages in `html` or `wikitext` (Wikipedia's internal markup language), which is not the friendliest for computers to read. 

Fortunately, `wikitext` has a decent bit of internal structure and is ~~easy~~ not impossible to work with.

This library provides a client that uses [wikitextparser](https://github.com/5j9/wikitextparser) (plus some custom logic) to convert wikitext into 
straightforward `json` objects (read: Python dictionaries) that you can use at your leisure.

It's much more comprehensive and accurate than [WiktionaryParser](https://github.com/Suyash458/WiktionaryParser) since it works with the raw wikitext rather than the generated html.

## One Wiktionary to rule them all.

There's one problem: Wiktionary is not one thing. 

No [there are 183 different Wiktionaries in 183 different languages](https://meta.wikimedia.org/wiki/Wiktionary#ListOfWiktionaries). 
Pretty much every single Wiktionary has its own, non-interoperable standards. So you have to have to build unique parsing logic for each Wiktionary.

(These are identified by the an [ISO 639 code](https://www.iso.org/iso-639-language-codes.html) subdomain (as in `en.wiktionary.com`))

So... we're starting with the English-language Wiktionary. Depending on how that goes, we might move on to additional wiktionaries.


# Structure

The current return structure is as follows:

```ts
{
  word: string,
  lang: string, // ISO language code
  altForms: LinkedWord[],
  etymology: LinkedWord[],
  pronunciations: (Pronunciation | Qualifier)[][],
  definitions: LinkedWord   
}[]

```

There is an entry for each 


# Example
Using the CLI to retrieve the English entries for "foo"

```sh
python wiktionary/cli.py foo en
```

Returns the following object, a list of entries (one for each unique etymology):

```json
[
  {
    "word": "foo",
    "lang": "en",
    "altForms": [],
    "etymology": [
      {
        "@id": "derived",
        "lang": "en",
        "srcLang": "cmn",
        "src": "府",
        "transliteration": "fǔ"
      },
      {
        "@id": "label",
        "lang": "en",
        "2": "historical",
        "3": "obsolete"
      }
    ],
    "pronunciations": [
      [
        {
          "@id": "dialect",
          "dialects": [
            "UK"
          ]
        },
        {
          "@id": "ipa",
          "lang": "en",
          "pronunciations": [
            {
              "ipa": "/fuː/"
            }
          ]
        }
      ],
      [
        {
          "@id": "En-au-foo.ogg",
          "lang": "en",
          "url": "Audio (AU)"
        }
      ],
      [
        {
          "@id": "rhymes",
          "lang": "en",
          "s": "1",
          "rhymes": [
            {
              "rhyme": "uː"
            }
          ]
        }
      ],
      [
        {
          "@id": "homophones",
          "lang": "en",
          "rhymes": [
            {
              "homophone": "-fu"
            }
          ]
        }
      ]
    ],
    "glyphOrigin": null,
    "description": null,
    "definitions": [
      {
        "@id": "references",
        "linked": [],
        "category": null,
        "data": "<references/>\n* [[rfc:3092]], ''Etymology of \"Foo\"'', {{w|Internet Engineering Task Force}} (IETF)\n\n"
      },
      {
        "@id": "anagrams",
        "linked": [
          {
            "@id": "anagram",
            "lang": "en",
            "alphagram": "foo",
            "anagrams": [
              "oof"
            ]
          }
        ]
      },
      {
        "@id": "noun",
        "data": []
      }
    ]
  },
  {
    "word": "foo",
    "lang": "en",
    "altForms": [],
    "etymology": [
      {
        "@id": "derived",
        "lang": "en",
        "srcLang": "zh",
        "src": "福",
        "alt": "",
        "gloss": "[[fortunate]]; [[prosperity]], [[good]] [[luck]]",
        "transliteration": "fú"
      },
      {
        "@id": "mention",
        "lang": "zh",
        "src": "福星",
        "alt": "",
        "gloss": "[[Jupiter]]",
        "transliteration": "Fúxīng"
      },
      {
        "@id": "mention",
        "lang": "en",
        "src": "om mani padme hum"
      },
      {
        "@id": "mention",
        "lang": "en",
        "src": "FUBAR"
      },
      {
        "@id": "label",
        "lang": "en",
        "2": "programming"
      },
      {
        "@id": "label",
        "lang": "en",
        "2": "fandom slang"
      },
      {
        "@id": "link",
        "lang": "en",
        "src": "foobar"
      },
      {
        "@id": "link",
        "lang": "en",
        "src": "FUBAR"
      }
    ],
    "pronunciations": [
      [
        {
          "@id": "dialect",
          "dialects": [
            "UK"
          ]
        },
        {
          "@id": "ipa",
          "lang": "en",
          "pronunciations": [
            {
              "ipa": "/fuː/"
            }
          ]
        }
      ],
      [
        {
          "@id": "En-au-foo.ogg",
          "lang": "en",
          "url": "Audio (AU)"
        }
      ],
      [
        {
          "@id": "rhymes",
          "lang": "en",
          "s": "1",
          "rhymes": [
            {
              "rhyme": "uː"
            }
          ]
        }
      ],
      [
        {
          "@id": "homophones",
          "lang": "en",
          "rhymes": [
            {
              "homophone": "-fu"
            }
          ]
        }
      ]
    ],
    "glyphOrigin": null,
    "description": null,
    "definitions": [
      {
        "@id": "references",
        "linked": [],
        "category": null,
        "data": "<references/>\n* [[rfc:3092]], ''Etymology of \"Foo\"'', {{w|Internet Engineering Task Force}} (IETF)\n\n"
      },
      {
        "@id": "anagrams",
        "linked": [
          {
            "@id": "anagram",
            "lang": "en",
            "alphagram": "foo",
            "anagrams": [
              "oof"
            ]
          }
        ]
      },
      {
        "@id": "noun",
        "data": [
          {
            "@id": "derivedTerms",
            "linked": [
              {
                "@id": "link",
                "lang": "en",
                "src": "foobar"
              }
            ]
          },
          {
            "@id": "relatedTerms",
            "linked": [
              {
                "@id": "link",
                "lang": "en",
                "src": "FUBAR"
              }
            ]
          }
        ]
      },
      {
        "@id": "derivedTerms",
        "linked": [
          {
            "@id": "link",
            "lang": "en",
            "src": "foobar"
          }
        ]
      },
      {
        "@id": "relatedTerms",
        "linked": [
          {
            "@id": "link",
            "lang": "en",
            "src": "FUBAR"
          }
        ]
      }
    ]
  },
  {
    "word": "foo",
    "lang": "en",
    "altForms": [],
    "etymology": [
      {
        "@id": "mention",
        "lang": "en",
        "src": "fuck"
      },
      {
        "@id": "sense",
        "sense": "expression of disgust"
      },
      {
        "@id": "link",
        "lang": "en",
        "src": "darn"
      },
      {
        "@id": "link",
        "lang": "en",
        "src": "drat"
      }
    ],
    "pronunciations": [
      [
        {
          "@id": "dialect",
          "dialects": [
            "UK"
          ]
        },
        {
          "@id": "ipa",
          "lang": "en",
          "pronunciations": [
            {
              "ipa": "/fuː/"
            }
          ]
        }
      ],
      [
        {
          "@id": "En-au-foo.ogg",
          "lang": "en",
          "url": "Audio (AU)"
        }
      ],
      [
        {
          "@id": "rhymes",
          "lang": "en",
          "s": "1",
          "rhymes": [
            {
              "rhyme": "uː"
            }
          ]
        }
      ],
      [
        {
          "@id": "homophones",
          "lang": "en",
          "rhymes": [
            {
              "homophone": "-fu"
            }
          ]
        }
      ]
    ],
    "glyphOrigin": null,
    "description": null,
    "definitions": [
      {
        "@id": "references",
        "linked": [],
        "category": null,
        "data": "<references/>\n* [[rfc:3092]], ''Etymology of \"Foo\"'', {{w|Internet Engineering Task Force}} (IETF)\n\n"
      },
      {
        "@id": "anagrams",
        "linked": [
          {
            "@id": "anagram",
            "lang": "en",
            "alphagram": "foo",
            "anagrams": [
              "oof"
            ]
          }
        ]
      },
      {
        "@id": "interjection",
        "data": [
          {
            "@id": "synonyms",
            "linked": [
              {
                "@id": "sense",
                "sense": "expression of disgust"
              },
              {
                "@id": "link",
                "lang": "en",
                "src": "darn"
              },
              {
                "@id": "link",
                "lang": "en",
                "src": "drat"
              }
            ]
          }
        ]
      },
      {
        "@id": "synonyms",
        "linked": [
          {
            "@id": "sense",
            "sense": "expression of disgust"
          },
          {
            "@id": "link",
            "lang": "en",
            "src": "darn"
          },
          {
            "@id": "link",
            "lang": "en",
            "src": "drat"
          }
        ]
      }
    ]
  },
  {
    "word": "foo",
    "lang": "en",
    "altForms": [
      {
        "word": {
          "@id": "link",
          "lang": "en",
          "src": "foo'"
        },
        "qualifiers": []
      }
    ],
    "etymology": [
      {
        "@id": "link",
        "lang": "en",
        "src": "foo'"
      },
      {
        "@id": "label",
        "lang": "en",
        "2": "slang"
      }
    ],
    "pronunciations": [
      [
        {
          "@id": "dialect",
          "dialects": [
            "UK"
          ]
        },
        {
          "@id": "ipa",
          "lang": "en",
          "pronunciations": [
            {
              "ipa": "/fuː/"
            }
          ]
        }
      ],
      [
        {
          "@id": "En-au-foo.ogg",
          "lang": "en",
          "url": "Audio (AU)"
        }
      ],
      [
        {
          "@id": "rhymes",
          "lang": "en",
          "s": "1",
          "rhymes": [
            {
              "rhyme": "uː"
            }
          ]
        }
      ],
      [
        {
          "@id": "homophones",
          "lang": "en",
          "rhymes": [
            {
              "homophone": "-fu"
            }
          ]
        }
      ]
    ],
    "glyphOrigin": null,
    "description": null,
    "definitions": [
      {
        "@id": "references",
        "linked": [],
        "category": null,
        "data": "<references/>\n* [[rfc:3092]], ''Etymology of \"Foo\"'', {{w|Internet Engineering Task Force}} (IETF)\n\n"
      },
      {
        "@id": "anagrams",
        "linked": [
          {
            "@id": "anagram",
            "lang": "en",
            "alphagram": "foo",
            "anagrams": [
              "oof"
            ]
          }
        ]
      },
      {
        "@id": "noun",
        "data": []
      }
    ]
  }
]
```
