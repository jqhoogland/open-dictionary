import isEmpty from "lodash/isEmpty";
import snakeCase from "lodash/snakeCase";
import { ISO639Schema } from "./iri";
import { JSONLDNode } from "./page";

const _flatten = (obj: any, ctx = ""): JSONLDNode[] => {
  if (Array.isArray(obj)) {
    return obj.flatMap((item) => _flatten(item, ctx));
  } else if (Object.keys(obj).includes("@template")) {
    if (ctx.length) {
      obj.ctx = ctx;
    }

    return obj;
  } else if (typeof obj === "object") {
    return Object.entries(obj).flatMap(([k, v]) => _flatten(v, `${ctx}/${k}`));
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

type Template = Record<string, string>;

export const parseTemplate = (template: string): Template => {
  template = template.slice(2, template.length - 2);
  const parts = template.split("|");
  const data: Record<string, string> = {};

  parts.forEach((part, i) => {
    if (part.includes("=")) {
      const [key, value] = part.split("=", 1) as [string, string];
      data[key] = value ?? true;
    } else if (i === 0) {
      data["@template"] = snakeCase(part);
    } else {
      data[i.toString()] = part;
    }
  });

  return data;
};

export const getTemplates =
  (parse: (t: Template) => Template) =>
  (text: string): Record<string, string>[] => {
    const templates = text.match(/{{[^}]+}}/g);
    if (templates === null) {
      return [];
    }
    return templates.map(parseTemplate);
  };
