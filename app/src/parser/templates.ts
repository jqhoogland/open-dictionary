import isEmpty from "lodash/isEmpty";
import snakeCase from "lodash/snakeCase";
import { ISO639Schema } from "./iri";
import { JSONLDNode } from "./page";
import yaml from "js-yaml";
import fs from "fs";
import path from "path";
import set from "lodash/set";

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

export type TemplateTransformMeta = {
  _id: string;
  _matches?: string[];
  _extends?: string[];
};

export type TemplateTransform = TemplateTransformMeta & {
  [key: Exclude<string, keyof TemplateTransformMeta>]: string;
};

export type Template = Record<string, string>;
export type Transformed<T extends Template> = T 

/** Reads a list of Trransform objects   */
export const loadTransforms = async (path: string) => {
  const transforms = yaml.load(fs.readFileSync(path, "utf-8"));
  return transforms as TemplateTransform[];
};

export const getTransform = (
  templateName: string,
  transforms: TemplateTransform[]
): TemplateTransform | undefined =>
  transforms.find((transform) => transform._match?.includes(templateName));


export const applyTransform = (
  inTemplate: Template,
  transform: TemplateTransform
): Transformed<Template> => {
  let template: Template = {
    "@type": transform._id,
  };

  for (let [kTransform, vTransform] of Object.entries(transform)) {
    // Check if meta tag (or an unallwoed value type)
    if ((["_match", "_id", "_extends"].includes(kTransform))) {
      continue;
    }if (typeof vTransform !== "string" || !vTransform) {
           console.error(
        "Invalid type of value. Only meta tags (_id, _match, _extends) are allowed to contain strings:", kTransform, vTransform);
    }

    for (let [kTemplate, vTemplate] of Object.entries(inTemplate)) {
      // With a direct match we can replace as is.
      if (kTemplate === kTransform) {
        set(template, vTransform, vTemplate);
        break;
      }
      
      // With a regex match, we may have to transform the value as well
      if (kTemplate.match(kTransform)) {
        // Only supported for matching integerss
        const kInt = parseInt(kTemplate); 
        const mV = vTransform.match(/\\1-(\d)/);

        if (mV && mV[1]) {
          const vIndex = parseInt(mV[1]);
          vTransform = vTransform.replace(/\\1-(\d)/, (kInt - vIndex).toString());
        }
        set(template, vTransform, vTemplate);
        break;
      }
    }
  }

  return template;
};

/** Reads a template in the original wiki template format 
 * 
 * I.e.: positional args are named "1",  "2", etc., and 
 * kwargs keep theiir original names.
*/
export const parseRawTemplate = (template: string): Template => {
  template = template.slice(2, template.length - 2);
  const parts = template.split("|");
  const data: Record<string, string> = {};

  parts.forEach((part, i) => {
    if (part.includes("=")) {
      const [key, value] = part.split("=", 1) as [string, string];
      data[key] = value ?? true;
    } else if (i === 0) {
      data._id = snakeCase(part);
    } else {
      data[i.toString()] = part;
    }
  });

  return data;
};

/** Given a string containing a wikitemplate `{{template_name|...}}`,
 * parses that string into an object using `parseRawTemplate`,
 * then transforms that object using the transformations returned by `transforrmLoader`. 
 */
export const transformTemplate = async (
  rawTemplateString: string,
  transformLoader: () => Promise<TemplateTransform[]>
): Promise<Transformed<Template>> => {
  const template = parseRawTemplate(rawTemplateString);
  const transforms = await transformLoader();
  const transform = getTransform(template._id!, transforms);

  if (!transform) {
    console.error(`No transform found for ${template._id}.`);
    return template;
  }

  return applyTransform(template, transform);
};

/** Given a string containing wiki templates 
 * (of the form `{{template_name|arg1|arg2...}}`),
 * 
 * Returns the result of mapping `parse` over these templates.
*/
export const getTemplates =
  (parse: (t: string) => Promise<Template>) =>
  async (text: string): Promise<Template[]> => {
    const templates = text.match(/{{[^}]+}}/g);
    if (templates === null) {
      return [];
    }
    return Promise.all(templates.map(parse));
  };
