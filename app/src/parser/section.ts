import { Expand } from "./../utils/types";
import { EntryQuery, langCodesToNames } from "./iri";
import set from "lodash/set";
import camelCase from "lodash/camelCase";
import snakeCase from "lodash/snakeCase";

const parseTemplate = (template: string): Record<string, string> => {
  template = template.slice(2, template.length - 2);
  const parts = template.split("|");
  const data: Record<string, string> = {};

  parts.forEach((part, i) => {
    if (part.includes("=")) {
      const [key, value] = part.split("=", 1) as [string, string];
      data[key] = value ?? true;
    } else if (i === 0) {
      data["@id"] = snakeCase(part);
    } else {
      data[(i + 1).toString()] = part;
    }
  });

  return data;
};

const getTemplates = (text: string): Record<string, string>[] => {
  const templates = text.match(/{{[^}]+}}/g);
  if (templates === null) {
    return [];
  }
  return templates.map(parseTemplate);
};

const getWikilinks = (text: string): Record<string, string>[] => {
  const wikilinks = text.match(/\[\[[^\]]+\]\]/g);
  if (wikilinks === null) {
    return [];
  }
  return wikilinks.map(parseTemplate);
};

interface Section extends Record<string, string[] | Section> {}

// TODO: Abandon this once rewiki is up and running
export const getSection = async (entryQuery: EntryQuery, text: string) => {
  const entryName = langCodesToNames[entryQuery.lang];
  let lines = text.split("\n");

  let start = -1;
  let end = 0;
  let line: string | null = null;

  let depth = 1;
  let sectionName = "preface";
  let section: Section = {};
  let items = [];

  for (let i = 0; i < lines.length; i++) {
    line = lines[i] as string;

    if (line === `==${entryName}==`) {
      start = i;
    } else if (/^==\b.+\b==$/.test(line)) {
      end = i;
      break;
    } else {
      let m = line.match(/^(=+)(\b.+)\b\1$/);
      if (m) {
        // Add current items to previous section
        let newDepth = m[1]!.length - 2;
        let newSectionName = camelCase(m[2]!);

        console.log({ newSectionName, sectionName, newDepth, depth });

        if (newDepth > depth) {
          // Down
          set(section, `${sectionName}.preface`, items);
          items = [];
          sectionName = `${sectionName}.${newSectionName}`;
        } else if (newDepth === depth) {
          // Same level
          set(section, sectionName, items);
          items = [];
          sectionName = newSectionName;
        } else {
          // Up
          const path = sectionName.split(".");
          const parent = path
            .slice(0, path.length - (depth - newDepth))
            .join(".");
          sectionName = parent ? `${parent}.${newSectionName}` : newSectionName;
        }

        depth = newDepth;
      }
    }
    items.push(...getTemplates(line));
    items.push(...getWikilinks(line));
  }

  lines = lines.splice(start, end - start);

  return section;
};
