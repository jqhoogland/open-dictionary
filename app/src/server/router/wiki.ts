import { EntryQuerySchema } from "../../parser/iri";
import { z } from "zod";
import { JSONLDNode, JSONLDSchema, parseWikiText } from "../../parser/page";
import { createRouter } from "./context";
import fs from "fs";
import { flatten } from "../../parser/en/templates";

const examplePage = fs.readFileSync("tests/example.wt", "utf8");
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
  // examplePage;
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
        path: "/wiki/json/{word}",
        summary: "Get entry JSON (nested)",
        description:
          "Parse the linked data contained on the corresponding wiktionary page",
      },
    },
    input: EntryQuerySchema,
    output: JSONLDSchema,
    async resolve({ input }) {
      return await getWikiText(input).then((text) =>
        parseWikiText(input, text)
      );
    },
  })
  .query("getWikiJsonLD", {
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
    output: z.any(), //JSONLDSchema,
    async resolve({ input }) {
      const data = await getWikiText(input).then((text) =>
        parseWikiText(input, text)
      );

      const { "@context": context, "@id": id, ...rest } = data;
      return {
        "@context": context,
        "@id": id,
        "@type": "od:Word",
        ...flatten(rest as any),
      };
    },
  });

export default wikiRouter;
