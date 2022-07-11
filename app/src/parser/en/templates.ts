import {
  getEntryIRI,
  getTemplateIRI,
  getWikiIRI,
  ISO639Schema,
} from "./../iri";
import z from "zod";
import isEmpty from "lodash/isEmpty";
import { JSONLDNode } from "../page";

const LangSchema = ISO639Schema;

// Schemas are structured so as first to consolidate aliases, then to apply tranforms.
const LTemplateSchema = z.object({
  "@template": z
    .enum(["l", "link"])
    .transform(() => getTemplateIRI({ template: "link" }, true)),
  "1": LangSchema,
  "2": z.string(),
});
//   .transform(({ "1": lang, "2": word, ...rest }, ctx) => ({
//     lang: getWikiIRI(lang, true),
//     "@id": getEntryIRI({ wiki: "en", lang, word }, true),
//     ...rest,
//   }));

const templateSchemas = [LTemplateSchema];

type WikiTemplate =
  | z.infer<typeof templateSchemas[number]>
  | Record<string, string>;

export const transformTemplate = (template: WikiTemplate) => {
  let type;

  for (let ts of templateSchemas) {
    // type = ts.innerType().shape["@type"];
    type = ts.shape["@template"];
    let names = Object.keys(type.innerType().Values);
    if ("@template" in names) {
      return ts.parse(template);
    }
  }

  if ("@template" in template) {
    template["@template"] = `en.wt.t:${template["@template"]}`;
  }

  // Fallback behavior is to leave the template as is
  return template;
};

export const enWiktionaryPlugin = () => {
  // TODO: Adjust this to work for a syntax tree
};

const _flatten = (obj: any, ctx = ""): JSONLDNode[] => {
  if (Array.isArray(obj)) {
    return obj.flatMap((item) => _flatten(item, ctx));
  } else if (Object.keys(obj).includes("@template")) {
    if (ctx.length) {
      obj.ctx = ctx;
    }

    return obj;
  } else if (typeof obj === "object") {
    return Object.entries(obj).flatMap(([k, v]) => _flatten(v, `${ctx}#${k}`));
  }
  return obj;
};

export const flatten = (obj: JSONLDNode): Record<string, JSONLDNode> => {
  const nodes = _flatten(obj);
  const data: Map<string, JSONLDNode> = new Map();

  let name: string;
  let prevNode: JSONLDNode | JSONLDNode[] | undefined;

  for (let node of nodes) {
    if (typeof node === "object") {
      // @ts-ignore
      if ("@template" in node && typeof node["@template"] === "string") {
        name = node["@template"] as string;
        prevNode = data.get(name);

        delete node["@template"];

        if (isEmpty(node)) {
          node = {
            "@value": true,
          };
        }

        if (name in data && !!prevNode) {
          if (Array.isArray(prevNode)) {
            // @ts-ignore
            data.set(name, [...prevNode, node!]);
          } else {
            data.set(name, [prevNode, node!]);
          }
        } else {
          data.set(name, node);
        }
      } else {
        console.log("ERROR", node);
      }
    }
  }
  // console.log({ ...data });

  return Object.fromEntries(data);
};
