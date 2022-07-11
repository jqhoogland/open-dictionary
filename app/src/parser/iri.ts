import { getBaseUrl } from "./../pages/_app";
import { z } from "zod";

export const langCodesToNames = {
  en: "English",
  es: "Spanish",
  fr: "French",
  de: "German",
  it: "Italian",
  ja: "Japanese",
  pt: "Portuguese",
} as const;

export type ISO639 = keyof typeof langCodesToNames;
export type LangName = typeof langCodesToNames[ISO639];

export const ISO639Schema = z.enum(
  Object.keys(langCodesToNames) as [ISO639, ...ISO639[]]
);

export const PageQuerySchema = z.object({
  wiki: ISO639Schema.default("en"),
  word: z.string().min(1),
});

export type PageQuery = z.infer<typeof PageQuerySchema>;

export const EntryQuerySchema = PageQuerySchema.merge(
  z.object({
    lang: ISO639Schema.default("en"),
  })
);

export type EntryQuery = z.infer<typeof EntryQuerySchema>;

export const getWikiIRI = (wiki: ISO639, prefix = false) =>
  prefix ? `wt-${wiki}:` : `https://${wiki}.wiktionary.org/wiki/`;

export const getPageIRI = (pageQuery: PageQuery, prefix = false) =>
  `${getWikiIRI(pageQuery.wiki, prefix)}${pageQuery.word}`;

export const getEntryIRI = (entryQuery: EntryQuery, prefix = false) =>
  `${getPageIRI(entryQuery, prefix)}#${langCodesToNames[entryQuery.lang]}`;

export const getBaseIRI = (prefix = false) => (prefix ? "od:" : getBaseUrl());

export const getContextIRI = (prefix = false) =>
  `${getBaseIRI(prefix)}/contexts/v1.json`;

export const getTemplateIRI = (
  { template, wiki = "en" }: { template: string; wiki?: ISO639 },
  prefix = false
) => `${getWikiIRI(wiki, prefix)}/Template:${template}`;
