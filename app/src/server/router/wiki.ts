import { z } from "zod";
import { createRouter } from "./context";

const EntryRequestSchema = z.object({
  word: z.string().min(1),
  lang: z.string().default("en"),
  wiki: z.string().default("en"),
});
interface WikiResponse {
  parse: {
    title: string;
    pageid: number;
    wikitext: {
      "*": string;
    };
  };
}

const getWikiText = async (input: z.infer<typeof EntryRequestSchema>) =>
  fetch(
    `https://${input?.wiki}.wiktionary.org/w/api.php?action=parse&page=${input.word}&format=json&prop=wikitext`
  )
    .then((res) => res.json())
    .then((res: WikiResponse) => res.parse.wikitext["*"]);

const wikiRouter = createRouter()
  .query("getWikiText", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/wiki/text/{word}",
        summary: "Get Wikitext",
        description: "Retrieve the wiktionary results for the given id",
      },
    },
    input: EntryRequestSchema,
    output: z.string(),
    async resolve({ input }) {
      return getWikiText(input);
    },
  })
  .query("getWikiJson", {
    meta: {
      openapi: {
        enabled: true,
        method: "GET",
        path: "/wiki/ld/{word}",
        summary: "Get entry JSON-LD",
        description:
          "Parse the linked data contained on the corresponding wiktionary page",
      },
    },
    input: EntryRequestSchema,
    output: z.string(),
    async resolve({ input }) {
      return getWikiText(input).then(parseWikitext);
    },
  });

export default wikiRouter;
