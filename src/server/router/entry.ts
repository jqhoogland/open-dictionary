import { createRouter } from "./context";
import { optional, z } from "zod";
import {
  languageSchema,
  defSchema,
  predicateSchema,
  pronunciationSchema,
  entrySchema,
  paginateSchema,
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
      language: languageSchema,
      word: z.string().min(1),
    }),
    output: entrySchema,
    async resolve({ input }) {
      return prisma.entry.findUniqueOrThrow({
        where: input,
        include: {
          definitions: {
            include: {
              sentences: true,
            },
          },
          pronunciations: true,
        },
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
      language: languageSchema,
    }),
    output: paginateSchema(entrySchema, z.number()),
    async resolve({ input: { limit, cursor, language } }) {
      const items = await prisma.entry.findMany({
        where: { language },
        take: limit,
        skip: cursor,
        orderBy: { rank: "desc" },
        cursor: { rank: cursor },
        include: {
          definitions: {
            include: {
              sentences: true,
            },
          },
          pronunciations: true,
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
      language: languageSchema,
      word: z.string(),
      rank: z.number(),
      definitions: z.array(defSchema),
      pronunciations: z.array(pronunciationSchema),
    }),
    output: entrySchema,
    async resolve({
      input: { language, word, rank, definitions, pronunciations },
    }) {
      const entry = await prisma.entry
        .create({
          data: {
            language,
            word,
            rank,
            definitions: {
              create: definitions.map(
                ({ partOfSpeech, definition, examples }, i) => ({
                  partOfSpeech,
                  rank: i,
                  sentences: {
                    create: [
                      {
                        predicateId: predicateSchema.enum.DEFINITION,
                        sentence: {
                          create: {
                            sentence: definition.value,
                            language: definition?.language ?? language,
                          },
                        },
                      },
                      ...examples.map((example) => ({
                        predicateId: predicateSchema.enum.EXAMPLE,
                        sentence: {
                          create: {
                            sentence: example,
                            language,
                          },
                        },
                      })),
                    ],
                  },
                })
              ),
            },
            pronunciations: {
              createMany: {
                data: pronunciations,
              },
            },
          },
        })
        .catch(console.error);

      console.log("[Entry:created]", entry);
      return entry;
    },
  });
