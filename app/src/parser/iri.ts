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

export const getWikiIRI = (wiki: ISO639) =>
  `https://${wiki}.wiktionary.org/wiki/`;

export const getPageIRI = (pageQuery: PageQuery) =>
  `${getWikiIRI(pageQuery.wiki)}${pageQuery.word}`;

export const getEntryIRI = async (entryQuery: EntryQuery) =>
  `${getPageIRI(entryQuery)}#${langCodesToNames[entryQuery.lang]}`;

export const getContextIRI = () => `${getBaseUrl()}/contexts/v1.json`;
