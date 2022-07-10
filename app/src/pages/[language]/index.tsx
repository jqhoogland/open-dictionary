import { createSSGHelpers } from "@trpc/react/ssg";
import { appRouter } from "../../server/router";
import type { GetStaticPropsContext, InferGetStaticPropsType } from "next";
import superjson from "superjson";
import BasicLayout from "../../components/BasicLayout";
import NavBar from "../../components/NavBar";
import { LANGUAGE_NAMES } from "../../utils/constants";
import { useRouter } from "next/router";
import type { Writable } from "type-fest";
import { Language } from "@prisma/client";
import { trpc } from "../../utils/trpc";
import React from "react";
import {
  Column,
  Table as ReactTable,
  PaginationState,
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  ColumnDef,
  OnChangeFn,
  flexRender,
} from "@tanstack/react-table";
import { z } from "zod";
import { BareEntrySchema } from "../../utils/validators";
import Link from "next/link";
import { TRPCRequestOptions } from "@trpc/react";
import { InferQueryOutput } from "../../server/trpc";
import { createContext } from "../../server/router/context";

type Entry = z.infer<typeof BareEntrySchema>;

function Table({
  language,
  data,
  columns,
  onLoadMore,
}: {
  language: Language;
  data: Entry[];
  columns: {
    header: string;
    columns: { accessorKey: keyof Entry }[];
  }[];
  onLoadMore: () => void;
}) {
  return (
    <table className="mt-8 w-full">
      <thead>
        <tr className="border-b-2 pb-4">
          <th className={"text-left w-20"}>Rank</th>
          <th className={"text-left w-80%"}>Word</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row) => {
          return (
            <Link href={`/${language}/${row.word}`} key={row.rank}>
              <tr className="hover:brightness-90 active:brightness-80 hover:cursor-pointer">
                <td>{row.rank}</td>
                <td>{row.word}</td>
              </tr>
            </Link>
          );
        })}
      </tbody>
      <tfoot>
        <tr>
          <td colSpan={2}>
            <button onClick={onLoadMore} className="btn btn-outline my-8">
              Load more
            </button>
          </td>
        </tr>
      </tfoot>
    </table>
  );
}

const LanguageOverview = (
  props: InferGetStaticPropsType<typeof getStaticProps>
) => {
  const router = useRouter();
  const { language } = props;
  const { data, fetchNextPage, ...rest } = trpc.useInfiniteQuery(
    ["entry.paginate", { language, limit: "10" }],
    {
      getNextPageParam: (lastPage) => lastPage?.nextCursor.toString(),
    }
  );
  const entries = React.useMemo(
    () => (data?.pages ?? []).flatMap(({ items }) => items),
    [data]
  );

  const columns = React.useMemo(
    () => [
      {
        header: "Rank",
        columns: [
          {
            accessorKey: "rank" as const,
          },
        ],
      },
      {
        header: "Word",
        columns: [
          {
            accessorKey: "word" as const,
          },
        ],
      },
    ],
    []
  );

  return (
    <BasicLayout>
      <NavBar language={language} />
      <main className="px-8 mx-auto max-w-screen-md py-16 min-h-[80vh]">
        <h1 className="text-6xl font-bold">
          {(LANGUAGE_NAMES as Writable<typeof LANGUAGE_NAMES>)[language]}
        </h1>
        <Table
          data={entries}
          columns={columns}
          language={language}
          onLoadMore={() => fetchNextPage()}
        />
      </main>
    </BasicLayout>
  );
};

export default LanguageOverview;

export async function getStaticProps({
  params,
  ...ctx
}: GetStaticPropsContext<{ language: Language }>) {
  const { language } = params!;

  const ssg = await createSSGHelpers({
    router: appRouter,
    ctx: await createContext(),
    transformer: superjson, // optional - adds superjson serialization
  });

  try {
    await ssg.fetchQuery("entry.paginate", {
      language,
      limit: "10",
    });
  } catch (e) {
    console.error(e);
  }

  return {
    props: {
      trpcState: ssg.dehydrate(),
      language,
    },
    revalidate: 1,
  };
}

export async function getStaticPaths() {
  return {
    paths: [],
    fallback: true, // false or 'blocking'
  };
}
