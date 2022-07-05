const { PrismaClient } = require('@prisma/client');
const PREDICATES = [
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
]
const prisma = new PrismaClient();

const capitalize = (s) => {
  if (!s) return "";
  return s.charAt(0).toUpperCase() + s.slice(1);
};

const seedPredicates = async() => {
  return prisma.predicate.createMany({
    data: PREDICATES.map((id) => ({
      id,
      name: capitalize(id.toLowerCase().replace("_", " ")),
    })),
  }).then(console.log);
};

seedPredicates();
