export const PREDICATES = [
  "DECLENSION",
  "CONJUGATION",
  "MUTATION",
  "ALTERNATIVE_RECONSTRUCTION",
  "SYNONYM",
  "ANTONYM",
  "HYPERNYM",
  "HYPONYM",
  "MERONYM",
  "HOLONYM",
  "TROPONYM",
  "COORDINATE_TERM",
  "DERIVED_TERM",
  "RELATED_TERM",
  "COLLOCATION",
  "DESCENDANT",
  "TRANSLATION",
  "ANAGRAM",

  // Sentence
  "EXAMPLE",
  "DEFINITION",
] as const;

export const PARTS_OF_SPEECH = [
  "ADJECTIVE",
  "ADVERB",
  "AMBIPOSITION",
  "ARTICLE",
  "CIRCUMPOSITION",
  "CLASSIFIER",
  "CONJUNCTION",
  "CONTRACTION",
  "COUNTER",
  "DETERMINER",
  "IDEOPHONE",
  "INTERJECTION",
  "NOUN",
  "NUMERAL",
  "PARTICIPLE",
  "PARTICLE",
  "POSTPOSITION",
  "PREPOSITION",
  "PRONOUN",
  "PROPER_NOUN",
  "VERB",

  // Morpheme
  "CIRCUMFIX",
  "COMBINING_FORM",
  "INFIX",
  "INTERFIX",
  "PREFIX",
  "ROOT",
  "SUFFIX",

  // "Symbol", "or", "Character",
  "DIACRITICAL_MARK",
  "LETTER",
  "LIGATURE",
  "NUMBER",
  "PUNCTUATION_MARK",
  "SYLLABLE",
  "SYMBOL",

  // "Phrase",
  "PHRASE",
  "PROVERB",
  "PREPOSITIONAL_PHRASE",
] as const;

export const LANGUAGE_NAMES = {
  en: "English",
  de: "Deutsch",
  fr: "Français",
  es: "Español",
  it: "Italiano",
  pt: "Português",
  ja: "日本語",
  zh: "中文",
  ko: "한국어",
  ru: "русский",
  // "ar": "العربية",
  // "el": "ελληνικά",
} as const;

export const LANGUAGES = Object.keys(
  LANGUAGE_NAMES
) as (keyof typeof LANGUAGE_NAMES)[];
