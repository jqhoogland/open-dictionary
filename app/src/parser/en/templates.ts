import z from "zod";
import { getTemplateIRI, ISO639Schema } from "./../iri";

const LangSchema = ISO639Schema;

const transformSchema
const transforms = new Map();

// Schemas are structured so as first to consolidate aliases, then to apply tranforms.
const LinkSchema = z.object({
  "@template": z.literal("l"),
  "1": LangSchema,
  "2": z.string(),
});
transforms.set("l", LinkSchema);
transforms.set("link", LinkSchema);

//   .transform(({ "1": lang, "2": word, ...rest }, ctx) => ({
//     lang: getWikiIRI(lang, true),
//     "@id": getEntryIRI({ wiki: "en", lang, word }, true),
//     ...rest,
//   }));

// Mention = TemplateMapping(
//   (name = "mention"),
//   (template_names = ["m", "mention", "m-self", "langname-mention"]),
//   (rename = Link.rename),
//   (ignore = Link.ignore)
// );

const MentionSchema = z.object({
  "1": LangSchema,
  "2": z.string(),
});
transforms.set("m", MentionSchema)
transforms.set("mention", MentionSchema)

const templateSchemas = [LinkSchema];

type WikiTemplate =
  | z.infer<typeof templateSchemas[number]>
  | Record<string, string>;

export const transformTemplate = (
  template: WikiTemplate,
  prefix = "en.wt.t:"
) => {
  let type;

  for (let ts of templateSchemas) {
    type = ts.shape["@template"];
    let names = Object.keys(type.innerType().Values);
    if ("@template" in names) {
      return ts.parse(template);
    }
  }

  if ("@template" in template) {
    template["@template"] = prefix + template["@template"];
  }

  // Fallback behavior is to leave the template as is
  return template;
};
