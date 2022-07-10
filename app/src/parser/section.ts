import { EntryQuery, langCodesToNames } from "./iri";

// TODO: Abandon this once rewiki is up and running
export const getSection = async (entryQuery: EntryQuery, text: string) => {
  const entryName = langCodesToNames[entryQuery.lang];
  let lines = text.split("\n");

  let start = -1;
  let end = 0;
  let line: string | null = null;

  for (let i = 0; i < lines.length; i++) {
    line = lines[i] as string;

    if (line === `==${entryName}==`) {
      start = i;
      continue;
    } else if (start < 0) {
      continue;
    }
    if (/^==\b.+\b==$/.test(line)) {
      end = i;
      break;
    }
  }

  lines = lines.splice(start, end - start);

  return lines;
};
