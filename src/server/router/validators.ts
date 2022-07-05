import { z } from "zod";
import { LANGUAGES, PARTS_OF_SPEECH, PREDICATES } from "./constants";

export const languageSchema = z.enum(LANGUAGES);

export const partOfSpeechSchema = z.enum(PARTS_OF_SPEECH);

export const defSchema = z.object({
  partOfSpeech: partOfSpeechSchema,
  definition: z.string().min(10),
  defLanguage: z.string(),
  examples: z.array(z.string()),
});

export const predicateSchema = z.enum(PREDICATES);

export const pronunciationSchema = z.object({
  broad: z.string().optional(),
  narrow: z.string().optional(),
});
