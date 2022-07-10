import {
  langCodesToNames,
  getEntryIRI,
  EntryQuery,
  getContextIRI,
} from "./iri";
import { string, z } from "zod";
import ontology from "../../../ontology/language.json";
import { Expand } from "../utils/types";
import { getSection } from "./section";

const JSONLDNodeSchema = z.string().or(z.array(z.string()));

export const JSONLDSchema = z
  .object({
    // TODO: Turn this into a url (& host the url)
    "@context": z.string(), // z.record(z.string(), z.string()),
    // The ID of the entry (e.g. "https://en.wiktionary.org/wiki/foo")
    "@id": z.string(),
  })
  .catchall(JSONLDNodeSchema);

type JSONLD = z.infer<typeof JSONLDSchema>;

export const parseWikiText = async (
  entryQuery: EntryQuery,
  wikitext: string
): Promise<JSONLD> => {
  const section = await getSection(entryQuery, wikitext);

  return {
    "@id": await getEntryIRI(entryQuery),
    "@context": getContextIRI(),
    page: wikitext,
    section: section ?? "",
  };
};
