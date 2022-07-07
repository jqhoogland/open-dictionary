import type { NextPage } from "next";
import BasicLayout from "../components/BasicLayout";
import Logo from "../components/Logo";
import SearchBar from "../components/SearchBar";

const Home: NextPage = () => {
  return (
    <BasicLayout>
      <main className="container flex flex-col items-center justify-center min-h-screen p-10 px-0 mx-auto md:py-20 md:p-10 md:px-0">
        <h1 className="font-extrabold text-center text-7xl">
          <Logo />
        </h1>

        <h3 className="items-center m-5 text-3xl">Wiktionary for machines (and exacting people).</h3>

        <section className="gap-10 p-5 w-full">
          <div className="w-full max-w-screen-md mx-auto">
            <SearchBar />
          </div>

          <div className="flex flex-row gap-5 justify-center p-5">
            <a href="/docs/rest/v1.html" className="text-stone-600 hover:text-stone-800 active:text-black">REST</a>
            <a className="text-stone-400 cursor-not-allowed">GraphQL (Coming Soon)</a>
          </div>
        </section>
      </main>
    </BasicLayout>
  );
};

export default Home;