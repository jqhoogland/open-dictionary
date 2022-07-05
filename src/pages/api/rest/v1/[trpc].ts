import { createOpenApiNextHandler } from "trpc-openapi";

import { appRouter } from "../../../../server/router";
import { createContext } from "../../../../server/router/context";

// Handle incoming OpenAPI requests
export default createOpenApiNextHandler({
  router: appRouter,
  createContext,
});
