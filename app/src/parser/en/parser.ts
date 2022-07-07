/**
 * For reference: https://en.wiktionary.org/wiki/Wiktionary:Entry_layout
 */

import { Language } from "@prisma/client";
import * as cheerio from "cheerio";
import fetch from "node-fetch";
import fs from "fs";
import { string } from "zod";

const HEADINGS_BEFORE_DEFS = [
  "Alternative forms",
  "Description",
  "Glyph origin",
  "Etymology",
  "Pronunciation",
] as const;

const PARTS_OF_SPEECH = [
  "Adjective",
  "Adverb",
  "Ambiposition",
  "Article",
  "Circumposition",
  "Classifier",
  "Conjunction",
  "Contraction",
  "Counter",
  "Determiner",
  "Ideophone",
  "Interjection",
  "Noun",
  "Numeral",
  "Participle",
  "Particle",
  "Postposition",
  "Preposition",
  "Pronoun",
  "Proper noun",
  "Verb",
];

const MORPHEMES = [
  "Circumfix",
  "Combining form",
  "Infix",
  "Interfix",
  "Prefix",
  "Root",
  "Suffix",
];

const SYMBOLS_AND_CHARACTERS = [
  "Diacritical mark",
  "Letter",
  "Ligature",
  "Number",
  "Punctuation mark",
  "Syllable",
  "Symbol",
];

const PHRASES = ["Phrase", "Proverb", "Prepositional phrase"];

const HAN_SPECIFIC = ["Han character", "Hanzi", "Kanji", "Hanja"];

const POS_HEADERS = [
  ...PARTS_OF_SPEECH,
  ...MORPHEMES,
  ...SYMBOLS_AND_CHARACTERS,
  ...PHRASES,
  ...HAN_SPECIFIC,
  "Romanization",
  "Logogram",
  "Determinative",
];

const HEADINGS_AFTER_DEFS = [
  "Usage notes",
  "Reconstruction notes",
  "Inflection, Declension or Conjugation",
  "Mutation",
  "Quotations",
  "Alternative forms",
  "Alternative reconstructions",
  "Synonyms",
  "Antonyms",
  "Hypernyms",
  "Hyponyms",
  "Meronyms",
  "Holonyms",
  "Troponyms",
  "Coordinate terms",
  "Derived terms",
  "Related terms",
  "Collocations",
  "Descendants",
  "Translations",
  "Trivia",
  "See also",
  "References",
  "Further reading",
  "Anagrams",
] as const;

type HeadingsBeforeDeps = typeof HEADINGS_BEFORE_DEFS[number];
type PartofSpeech = typeof PARTS_OF_SPEECH[number];
type Morphemes = typeof MORPHEMES[number];
type SymbolsAndCharacters = typeof SYMBOLS_AND_CHARACTERS[number];
type Phrases = typeof PHRASES[number];
type HanSpecific = typeof HAN_SPECIFIC[number];
type PosHeaders = typeof POS_HEADERS[number];
type HeadingsAfterDeps = typeof HEADINGS_AFTER_DEFS[number];

type SoftAutocomplete<T extends string> = T | Omit<string, T>;

type LinkedWord = string;
type ContextLabel = string; // Look for href, strip /wiki/ (#id can be important)
type ExampleSentence = {
  // Invented by a Wiktionary author
  // Specialized formats for Chinese, Japanese, & Korean
  // We're ignoring non-ux-templated ones for now
};
type Quotations = {
  // Invented by someone else
};

interface AbbreviationDetails {
  expandedForm: LinkedWord;
  wikipediaLink: LinkedWord;
  subcomponentLinks: LinkedWord[];
}

interface WiktionaryDefinition {
  abbreviation?: AbbreviationDetails;
  contextLabel?: ContextLabel;
  examples?: ExampleSentence[];
  quotations?: Quotations[];
}

interface PartOfSpeechSection {
  // Where the word is repeated with romanization if applicable.
  // Plus additional info like inflected forms
  headwordLine: string;
  definitions: WiktionaryDefinition[];
  usageNotes: string;
  synonyms: string;
  antonyms: string;
  hypernyms: string;
  hyponyms: string;
  meronyms: string;
  holonyms: string;
  troponyms: string;
  coordinateTerms: string;
  derivedTerms: string;
  relatedTerms: string;
  collocations: string;
  descendants: string;
  translations: string;
}

interface WiktionaryPronunciation {
  phoneticTranscriptions: string[];
  audioFiles: string[];
  rhymes: string[];
  homophones: string[];
  hyphenation: string[];
}

type WiktionaryEntry = {
  alternativeForms?: string[];
  description?: string;
  etymology: string;
  glyphOrigin?: string;
  pronunciation?: WiktionaryPronunciation;
  references?: string;
  furtherReading?: string;
  anagrams?: string;
} & {
  [key in PosHeaders]: PartOfSpeechSection;
};

// @ts-ignore
type Ch = cheerio.Cheerio;
type El = cheerio.Element;

const parseTranscriptionType = (s: string) => {
  if (s.startsWith("/")) return "broad";
  if (s.startsWith("[")) return "narrow";
  return "";
};

const parsePronunciation = ($: cheerio.CheerioAPI, section: Ch) =>
  section
    .map((i: number, li: El) => {
      const ipa =
        $(li as any)
          .find("span.IPA")
          .html() ?? "";

      return {
        ipa: ipa.length > 1 ? ipa.slice(1, ipa.length - 1) : null,
        type: parseTranscriptionType(ipa),
      };
    })
    .get();

const fetchEntry = async (word: string, language: Language) => {
  // return fetch(`https://${language}.wiktionary.org/wiki/${word}`)
  //  .then((res) => res.text())
  const file = fs.readFileSync("./test.html");
  const doc = file.toString();
  const $ = cheerio.load(doc);

  const englishSection = $("<div>").append(
    $("span#English").parent("h2").nextUntil("h2")
  );
  return {
    pronunciation: parsePronunciation(
      // @ts-ignore
      $,
      englishSection.find("#Pronunciation").parent().next("ul")
    ),
  };
};

// @ts-ignore
console.log(await fetchEntry("hello", "en"));
