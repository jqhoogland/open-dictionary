import { transformWikiLink } from "../wikilinks";

export const transformEnWikiLink = async (wl: string, prefix = "en.wt.t:") =>
  transformWikiLink(wl); // TODO: Add wiktionary-specific parasing
