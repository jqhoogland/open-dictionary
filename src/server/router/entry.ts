import { createRouter } from "./context";
import { optional, z } from "zod";
import {
  languageSchema,
  defSchema,
  predicateSchema,
  pronunciationSchema,
} from "./validators";

const entrySchema = z.object({
  word: z.string().min(1),
  language: languageSchema,
  createdAt: z.date(),
  updatedAt: z.date(),
  rank: z.number(),
  definitions: z.array(defSchema),
  pronunciations: z.array(pronunciationSchema),
});

const paginateSchema = <T extends z.ZodType>(item: T, cursor: z.ZodType) =>
  z.object({
    data: z.array(item),
    cursor,
  });

export const entryRouter = createRouter()
  .query("get", {
    meta: {
      openapi: { enabled: true, method: "GET", path: "/{language}/{word}" },
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
      openapi: { enabled: true, method: "GET", path: "/{language}" },
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
      const data = await prisma.entry.findMany({
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
        data,
        cursor: data.length === limit ? cursor + data.length : null,
      };
    },
  })
  .mutation("create", {
    meta: {
      openapi: { enabled: true, method: "POST", path: "/{language}" },
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
      return prisma.entry.create({
        data: {
          language,
          word,
          rank,
          definitions: {
            create: definitions.map(
              ({ partOfSpeech, definition, defLanguage, examples }, i) => ({
                partOfSpeech,
                rank: i,
                sentences: {
                  create: [
                    {
                      predicateId: predicateSchema.enum.DEFINITION,
                      sentence: {
                        create: {
                          sentence: definition,
                          language: defLanguage,
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
            create: pronunciations.map((pronunciation) => ({
              ...pronunciation,
              word,
              language,
            })),
          },
        },
      });
    },
  });
