import { Definition } from "@prisma/client";
import { MergeExclusive } from "type-fest";
import { z } from "zod";
import { LANGUAGES, PARTS_OF_SPEECH, PREDICATES } from "./constants";

// Numbers
export const WholeNumberSchema = z.number().int().nonnegative();
export const BigIntSchema = z
  .bigint()
  .transform((int) => Number(int))
  .or(z.number());
export const StringifiedInt = z.string().transform((int) => parseInt(int));

// Enums
export const LanguageSchema = z.enum(LANGUAGES);
export const PartOfSpeechSchema = z
  .enum(PARTS_OF_SPEECH)
  .describe(
    "See [English Wikipedia's layout conventions](https://en.wiktionary.org/wiki/Wiktionary:Entry_layout#Part_of_speech)"
  );
export const PredicateSchema = z.enum(PREDICATES);

// Common object fragments
export const TimesSchema = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
});

export const WordAndLanguageSchema = z.object({
  word: z.string(),
  language: LanguageSchema,
});

// Definitions

export const BareSentenceSchema = z.object({
  id: z.string(),
  sentence: z.string(),
});

export const SentenceSchema = BareSentenceSchema.merge(TimesSchema).extend({
  language: LanguageSchema,
});

export const BareSentenceTripleSchema = z.object({
  predicateId: z.string(),
  detail: z.string().nullable().optional(),
  sentence: BareSentenceSchema,
});

export const SentenceTripleSchema = BareSentenceTripleSchema.extend({
  defId: z.string(),
  sentenceId: z.string(),
}).merge(TimesSchema);

export const BareDefinitionSchema = z.object({
  id: z.string(),
  sentences: z.array(BareSentenceTripleSchema),
});

export const DefinitionBaseSchema = z.object({
  partOfSpeech: PartOfSpeechSchema,
  examples: z.array(z.string()),
});

export const CreateDefinitionSchema = DefinitionBaseSchema.extend({
  definitions: z.array(
    z.object({
      sentence: z.string().min(2),
      language: LanguageSchema.optional().describe(
        "Defaults to the language of the corresponding word."
      ),
    })
  ),
});

export const DefinitionSchema = DefinitionBaseSchema.extend({
  id: z.string(),
  partOfSpeech: PartOfSpeechSchema,
  definitions: z.array(
    z.object({
      sentence: z.string(),
      language: LanguageSchema,
    })
  ),
  examples: z.array(z.string()),
  rank: z.number(),
  word: z.string(),
})
  .merge(TimesSchema)
  .merge(WordAndLanguageSchema);

// Pronunciations

export const PronunciationBaseSchema = z.object({
  broad: z.string().nullable(),
  narrow: z.string().nullable(),
  description: z.string().nullable(),
});

export const CreatePronunciationSchema = PronunciationBaseSchema.partial();

export const PronunciationSchema = PronunciationBaseSchema.merge(TimesSchema);

// Entries

export const EntryWithoutIncludesSchema = z
  .object({
    rank: BigIntSchema,
  })
  .merge(TimesSchema)
  .merge(WordAndLanguageSchema);

export const BareEntrySchema = z.object({
  word: z.string().min(1),
  rank: BigIntSchema,
  definitions: z.array(BareDefinitionSchema),
});

export const EntrySchema = BareEntrySchema.extend({
  language: LanguageSchema,

  // pronunciations: z.array(CreatePronunciationSchema),
}).merge(TimesSchema);

// Utils

export const paginateSchema = <T extends z.ZodType>(
  item: T,
  cursor: z.ZodType
) =>
  z.object({
    items: z.array(item),
    nextCursor: cursor.nullable(),
  });
