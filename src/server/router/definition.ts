import { Definition } from "@prisma/client";
import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { prisma } from "../db/client";
import { createRouter } from "./context";
import {
  LanguageSchema,
  CreateDefinitionSchema,
  PartOfSpeechSchema,
  DefinitionSchema,
  WholeNumberSchema,
  StringifiedInt,
} from "./validators";
import type { SetOptional } from "type-fest";

const defSentenceSchema = z.object({
  language: LanguageSchema,
  definition: z.string(),
});

export const definitionRouter = createRouter()
  .query("get", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/definition/{id}",
        summary: "Read definition",
        description: "Retrieve definition with the given id",
      },
    },
    input: z.object({
      id: z.string().min(1),
    }),
    output: CreateDefinitionSchema,
    async resolve({ input }) {
      return prisma.definition.findUniqueOrThrow({
        where: input,
      });
    },
  })
  .query("getByRank", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/{language}/{word}/{partOfSpeech}/definition/{rank}",
        summary: "Read definition",
        description: "Retrieve definition with the given id",
      },
    },
    input: z.object({
      language: LanguageSchema,
      partOfSpeech: PartOfSpeechSchema,
      word: z.string().min(1),
      rank: StringifiedInt,
    }),
    output: DefinitionSchema,
    async resolve({ input }) {
      return prisma.definition.findUniqueOrThrow({
        where: { word_language_partOfSpeech_rank: input },
      });
    },
  })
  .query("listByWord", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/{language}/{word}/definition",
        summary: "List definitions",
        description: "List definitions for entries in `language`.",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string().min(1),
    }),
    output: z.array(DefinitionSchema),
    async resolve({ input }) {
      return (
        await prisma.definition.findMany({
          where: input,
          include: {
            sentences: {
              include: {
                sentence: true,
              },
            },
          },
        })
      ).map(({ sentences, ...rest }) => {
        const definitions = sentences
          .filter(({ predicateId }) => predicateId === "DEFINITION")
          .map(({ sentence }) => ({
            language: sentence.language,
            sentence: sentence.sentence,
          }));
        const examples = sentences
          .filter(({ predicateId }) => predicateId === "EXAMPLE")
          .map(({ sentence }) => sentence.sentence);

        return {
          ...rest,
          definitions,
          examples,
        };
      });
    },
  })
  .mutation("create", {
    meta: {
      openapi: {
        enabled: true,
        method: "POST",
        path: "/{language}/{word}/definition",
        summary: "Create definition",
        description: "Create a new definition for `word` in `language`",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string(),
      partOfSpeech: PartOfSpeechSchema,
      rank: z.number(),
      sentences: z.array(defSentenceSchema),
      examples: z.array(z.string()).default([]),
    }),
    output: DefinitionSchema,
    async resolve({ input: { sentences, examples, ...input } }) {
      if (
        await prisma.definition.findFirst({
          where: input,
        })
      ) {
        throw new TRPCError({
          code: "BAD_REQUEST",
          message: "Definition already exists",
        });
      }

      const newDefinition = (await prisma.definition.create({
        data: input,
      })) as SetOptional<
        z.infer<typeof DefinitionSchema>,
        "definitions" | "examples"
      >;

      // TODO: More efficient creates + single transaction
      newDefinition.definitions = await Promise.all(
        sentences.map(async ({ language, definition: sentence }) =>
          prisma.sentence.create({
            data: {
              language,
              sentence,
              definitions: {
                create: {
                  defId: newDefinition.id,
                  predicateId: "DEFINITION",
                },
              },
            },
          })
        )
      );

      examples.map(async (example) =>
        prisma.sentence.create({
          data: {
            language: input.language,
            sentence: example,
            definitions: {
              create: {
                defId: newDefinition.id,
                predicateId: "EXAMPLE",
              },
            },
          },
        })
      );

      newDefinition.examples = examples;
      console.log(newDefinition);
      return newDefinition;
    },
  });
