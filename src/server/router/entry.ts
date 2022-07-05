import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { prisma } from "./../db/client";
import { createRouter } from "./context";
import {
  EntrySchema,
  EntryWithoutIncludesSchema,
  LanguageSchema,
  paginateSchema,
  WholeNumberSchema,
} from "./validators";

export const entryRouter = createRouter()
  .query("get", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/{language}/{word}",
        summary: "Read entry",
        description:
          "Retrieve definitions and pronunciations for `word` in `language`",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string().min(1),
    }),
    output: EntryWithoutIncludesSchema,
    async resolve({ input }) {
      return prisma.entry.findUniqueOrThrow({
        where: { word_language: input },
      });
    },
  })
  .query("paginate", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/{language}",
        summary: "Paginate entries",
        description:
          "Paginate definitions and pronunciations for entries in `language`, ordered by word frequency.",
      },
    },
    input: z.object({
      limit: z
        .string()
        .transform((s) => parseInt(s))
        .default("10")
        .describe("A number < 100"),
      cursor: z
        .string()
        .transform((s) => parseInt(s))
        .default("0")
        .describe("A number"),
      language: LanguageSchema,
    }),
    output: paginateSchema(EntrySchema, z.number()),
    async resolve({ input: { limit, cursor, language } }) {
      const items = await prisma.entry.findMany({
        where: { language },
        take: limit,
        skip: cursor,
        orderBy: { rank: "desc" },
        include: {
          definitions: {
            select: {
              id: true,
              sentences: true,
            },
          },
          // pronunciations: true,
        },
      });
      return {
        items,
        cursor: items.length === limit ? cursor + items.length : null,
      };
    },
  })
  .mutation("create", {
    meta: {
      openapi: {
        enabled: true,
        method: "POST",
        path: "/{language}",
        summary: "Create entry",
        description: "Create a new entry for `word` in `language`",
      },
    },
    input: z.object({
      language: LanguageSchema,
      word: z.string().min(1),
      rank: WholeNumberSchema.optional(),
    }),
    output: EntryWithoutIncludesSchema,
    async resolve({ input: { language, word, rank: _rank } }) {
      let rank = _rank;

      if (
        rank &&
        (await prisma.entry.findUnique({
          where: { rank_language: { language, rank } },
        }))
      ) {
        throw new TRPCError({
          code: "BAD_REQUEST",
          message: "Given rank already exists for language",
        });
      } else if (!rank) {
        rank = (await prisma.entry.count({ where: { language } })) + 1;
      }

      return prisma.entry.create({
        data: {
          language,
          word,
          rank,
        },
      });
    },
  });
