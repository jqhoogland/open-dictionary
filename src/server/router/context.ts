// src/server/router/context.ts
import * as trpc from "@trpc/server";
import * as trpcNext from "@trpc/server/adapters/next";
import { unstable_getServerSession as getServerSession } from "next-auth";

import { authOptions as nextAuthOptions } from "../../pages/api/auth/[...nextauth]";
import { prisma } from "../db/client";
import { OpenApiMeta } from "trpc-openapi";
import next from "next";

export const createContext = async (
  opts?: trpcNext.CreateNextContextOptions
) => {
  const req = opts?.req;
  const res = opts?.res;

  const session = false;
  //  req && res && (await getServerSession(req, res, nextAuthOptions));

  return {
    req,
    res,
    session,
    prisma,
  };
};

type Context = trpc.inferAsyncReturnType<typeof createContext>;

export const createRouter = () =>
  trpc.router<Context, OpenApiMeta>().middleware((opts) => {
    console.log(opts?.meta?.openapi?.method, opts?.meta?.openapi?.path);
    return opts.next();
  });
