import { parseTemplate } from "./templates";

export const getWikilinks = (text: string): Record<string, string>[] => {
  const wikilinks = text.match(/\[\[[^\]]+\]\]/g);
  if (wikilinks === null) {
    return [];
  }
  return wikilinks.map(parseTemplate);
};
