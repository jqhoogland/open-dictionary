import { z } from "zod";
import { LANGUAGES, PARTS_OF_SPEECH, PREDICATES } from "./constants";

export const languageSchema = z.enum(LANGUAGES);

export const partOfSpeechSchema = z
  .enum(PARTS_OF_SPEECH)
  .describe(
    "See [English Wikipedia's layout conventions](https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech)"
  );

export const defSchema = z.object({
  partOfSpeech: partOfSpeechSchema,
  definition: z.object({
    value: z.string().min(2),
    language: z
      .enum(LANGUAGES)
      .optional()
      .describe("Defaults to the language of the corresponding word."),
  }),
  examples: z.array(z.string()),
});

export const predicateSchema = z.enum(PREDICATES);

export const pronunciationSchema = z.object({
  broad: z.string().optional(),
  narrow: z.string().optional(),
  description: z.string().optional(),
});

export const entrySchema = z.object({
  word: z.string().min(1),
  language: languageSchema,
  createdAt: z.date(),
  updatedAt: z.date(),
  rank: z.number(),
  definitions: z.array(defSchema),
  pronunciations: z.array(pronunciationSchema),
});

export const paginateSchema = <T extends z.ZodType>(
  item: T,
  cursor: z.ZodType
) =>
  z.object({
    items: z.array(item),
    cursor: cursor.nullable(),
  });
