import { Template } from "./templates";

export interface WikiLink {
  link?: string;
  extra?: string[];
}

export const transformWikiLink = (wl: string): WikiLink => {
  const parts = wl.slice(2, wl.length - 2).split("|");
  return {
    link: parts[0],
    extra: parts.slice(1, parts.length),
  };
};

export const getWikilinks =
  (parse: (wl: string) => Promise<Template>) =>
  async (text: string): Promise<WikiLink[]> => {
    const wikilinks = text.match(/\[\[[^\]]+\]\]/g);
    if (!wikilinks) {
      return [];
    }
    return Promise.all(wikilinks.map(parse));
  };
