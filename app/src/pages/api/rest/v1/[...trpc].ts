import { createOpenApiNextHandler } from "trpc-openapi";

import { appRouter } from "../../../../server/router";
import { createContext } from "../../../../server/router/context";

// Handle incoming OpenAPI requests
export default createOpenApiNextHandler({
  router: appRouter,
  createContext,
  onError({ error, type, path, input, ctx, req }) {
    console.error("Error:", error);
    if (error.code === "INTERNAL_SERVER_ERROR") {
      // send to bug reporting
    }
  },
});
