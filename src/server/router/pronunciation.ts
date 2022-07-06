import { z } from "zod";
import { prisma } from "../db/client";
import { createRouter } from "./context";
import {
  LanguageSchema,
  CreatePronunciationSchema,
  PronunciationSchema,
} from "../../utils/validators";

export const pronunciationRouter = createRouter()
  .query("get", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/pronunciation/{id}",
        summary: "Read pronunciation",
        description: "Retrieve pronunciation with the given id",
      },
    },
    input: z.object({
      id: z.string().min(1),
    }),
    output: CreatePronunciationSchema,
    async resolve({ input }) {
      return prisma.pronunciation.findUniqueOrThrow({
        where: input,
      });
    },
  })
  .query("listByWord", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/{language}/{word}/pronunciation",
        summary: "List pronunciations",
        description: "List pronunciations for entries in `language`.",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string().min(1),
    }),
    output: z.array(CreatePronunciationSchema),
    async resolve({ input }) {
      return await prisma.pronunciation.findMany({
        where: input,
      });
    },
  })
  .mutation("create", {
    meta: {
      openapi: {
        enabled: true,
        method: "POST",
        path: "/{language}/{word}/pronunciation",
        summary: "Create pronunciation",
        description: "Create a new pronunciation for `word` in `language`",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string(),
      defId: z.string().optional(),
      sentenceId: z.string().optional(),
      narrow: z.string().optional(),
      broad: z.string().optional(),
      coordinates: z
        .object({
          latitude: z.number().min(-90).max(90),
          longitude: z.number().min(-180).max(180),
        })
        .optional()
        .describe("Currently not in use."),
      hyphenation: z.string().optional(),
      description: z.string().optional(),
    }),
    output: PronunciationSchema,
    async resolve({ input: { coordinates, ...input } }) {
      return prisma.pronunciation.create({
        data: input,
      });
    },
  });
