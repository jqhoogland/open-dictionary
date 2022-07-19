import { applyTransform, transformTemplate } from "./../templates";
import z from "zod";
import { getTransform, loadTransforms, TemplateTransform } from "../templates";
import { getTemplateIRI, ISO639Schema } from "./../iri";
import path from "path";

const LangSchema = ISO639Schema;

type WikiTemplate = Record<string, string>;

let transforms: TemplateTransform[];

export const loadEnTransforms = async () => {
  transforms =
    // Fix paths
    transforms ??
    loadTransforms(
      "/Users/Jesse/Projects/open-dictionary/app/public/en/template.yaml"
    );
  return transforms;
};

export const transformEnTemplate = async (
  template: string,
  prefix = "en.wt.t:"
) => transformTemplate(template, loadEnTransforms);
