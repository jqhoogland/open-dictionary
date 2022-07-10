import { definitionRouter } from "./definition";
// src/server/router/index.ts
import { createRouter } from "./context";
import superjson from "superjson";

import { entryRouter } from "./entry";
import { pronunciationRouter } from "./pronunciation";
import wikiRouter from "./wiki";
// import { authRouter } from "./auth";

export const appRouter = createRouter()
  .transformer(superjson)
  .merge("wiki.", wikiRouter)
  .merge("entry.", entryRouter)
  .merge("pronunciation.", pronunciationRouter)
  .merge("definition.", definitionRouter);
//  .merge("auth.", authRouter);

// export type definition of API
export type AppRouter = typeof appRouter;
