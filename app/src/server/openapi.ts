import { generateOpenApiDocument } from "trpc-openapi";

import { appRouter } from "./router";

export const openApiDocument = generateOpenApiDocument(appRouter, {
  title: "OpenDictionary API",
  version: "1.0.0",
  baseUrl: "http://localhost:3000",
});
