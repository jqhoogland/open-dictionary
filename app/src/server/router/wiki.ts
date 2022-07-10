import { z } from "zod";
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

const wikiRouter = createRouter().query("getWikitext", {
  meta: {
    openapi: {
      enabled: true,
      method: "GET",
      path: "/wiki/text/{word}",
      summary: "Read a result from the wiktionary api",
      description: "Retrieve the wiktionary results for the given id",
    },
  },
  input: z.object({
    word: z.string().min(1),
    lang: z.string().default("en"),
    wiki: z.string().default("en"),
  }),
  output: z.string(),
  async resolve({ input }) {
    return fetch(
      `https://${input?.wiki}.wiktionary.org/w/api.php?action=parse&page=${input.word}&format=json&prop=wikitext`
    )
      .then((res) => res.json())
      .then((res: WikiResponse) => res.parse.wikitext["*"]);
  },
});

export default wikiRouter;
