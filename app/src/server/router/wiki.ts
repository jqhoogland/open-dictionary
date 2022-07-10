import { EntryQuerySchema } from "../../parser/iri";
import { z } from "zod";
import { JSONLDSchema, parseWikiText } from "../../parser/page";
import { createRouter } from "./context";

interface WikiResponse {
  parse: {
    title: string;
    pageid: number;
    wikitext: {
      "*": string;
    };
  };
}

const getWikiText = async (input: z.infer<typeof EntryQuerySchema>) =>
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
    input: EntryQuerySchema,
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
    input: EntryQuerySchema,
    output: JSONLDSchema,
    async resolve({ input }) {
      return getWikiText(input).then((text) => parseWikiText(input, text));
    },
  });

export default wikiRouter;
