// Han characters and language-specific varieties: Han character, Hanzi, Kanji, Hanja
// Romanization
// Logogram
// Determinative

type PredicateType =
  | "DECLENSION" // Inflection of nouns, adjectives, etc.
  | "CONJUGATION" // Inflection of verbs
  | "MUTATION"
  | "ALTERNATIVE_RECONSTRUCTION"
  | "SYNONYM"
  | "ANTONYM"
  | "HYPERNYM"
  | "HYPONYM"
  | "MERONYM"
  | "HOLONYM"
  | "TROPONYM"
  | "COORDINATE_TERM"
  | "DERIVED_TERM"
  | "RELATED_TERM"
  | "COLLOCATION"
  | "DESCENDANT"
  | "TRANSLATION"
  | "ANAGRAM";

/**
 * Where it gets confusing.
 *
 * Words exist in:
 * - Phonetic space. They correspond to a "sound".
 * - Semantic space. They correspond to a "meaning".
 * - Lexical space. They correspond to a "written word".
 *
 * Sometimes, these overlap neatly. Those are the exceptions.
 *
 * Most words have dozens of equally valid intra- and even interpersonally varying pronunciations.
 * Many have multiple, even contradictory meanings.
 * Fortunately, writing is usually more consistent. It gets tricky when people use different scripts all over the place.
 *
 */

const PREDICATES = [
  // Alternative Forms
  "REGIONAL",
  "HISTORICAL",
  "HYPHENIZATION",
  "COMPOUND",
  "STYLE",
  "UNCERTAIN_CAPITALIZATION",
  "SCRIPT",
];
