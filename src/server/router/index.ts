// src/server/router/index.ts
import { createRouter } from "./context";
import superjson from "superjson";

import { entryRouter } from "./entry";
// import { authRouter } from "./auth";

export const appRouter = createRouter()
  .transformer(superjson)
  .merge("entry.", entryRouter);
//  .merge("auth.", authRouter);

// export type definition of API
export type AppRouter = typeof appRouter;
