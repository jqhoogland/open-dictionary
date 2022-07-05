import type { NextPage } from "next";
import Head from "next/head";
import FaviconEmoji from "../components/FaviconEmoji";
import { trpc } from "../utils/trpc";
import { LANGUAGES, LANGUAGE_NAMES } from "../server/router/constants";
import React from "react";
import { ChevronUpIcon, ChevronDownIcon } from "@heroicons/react/solid"
import { useRouter } from "next/router";

const SearchBar: React.FC = () => {
  const router = useRouter();
  const [activeLanguage, setActiveLanguage] = React.useState("en");

  const handleKeyDown = React.useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.code === "Enter") {
      e.preventDefault();
      router.push(`/${activeLanguage}/${e.target!.value}`);
    }
  }, [])

  return (
    <fieldset className="relative">
      <input type="text" placeholder="Search" className="input input-bordered w-full" onKeyDown={handleKeyDown} />
      <select className="absolute !min-h-0 h-auto py-0.5 pl-4 pr-8 top-2 bottom-2 right-2 select select-ghost">
        {LANGUAGES.map((language) => (
          <option
            key={language}
            value={language}
            id={`select-item-${language}`}
            className="btn btn-ghost w-full"
          >
            {LANGUAGE_NAMES[language]}
          </option>
        ))}
      </select>
    </fieldset >
  )
}

const Home: NextPage = () => {
  return (
    <>
      <Head>
        <title>OpenDictionary</title>
        <meta name="description" content="Machine Readable Wiktionary" />
        <FaviconEmoji>{"📖"}</FaviconEmoji>
      </Head>

      <div className="container flex flex-col items-center justify-center min-h-screen p-10 px-0 mx-auto md:py-20 md:p-10 md:px-0">
        <h1 className="font-extrabold text-center text-7xl">
          {"📖"} Open<span className="text-blue-500">Dictionary</span>
        </h1>

        <h3 className="items-center m-5 text-3xl">Wiktionary for machines (and precise people).</h3>

        <main className="gap-10 p-5 w-full">
          <section className="w-full max-w-screen-md mx-auto">
            <SearchBar />
          </section>

          <section className="flex flex-row gap-5 justify-center p-5">
            <a href="/docs/rest/v1.html" className="text-stone-600 hover:text-stone-800 active:text-black">REST</a>
            <a className="text-stone-400 cursor-not-allowed">GraphQL (Coming Soon)</a>
          </section>
        </main>
      </div>
    </>
  );
};

export default Home;