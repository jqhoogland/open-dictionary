import Link from "next/link";
import { useRouter } from "next/router";
import BasicLayout from "../../components/BasicLayout";
import Logo from "../../components/Logo";
import SelectLanguage from "../../components/SelectLanguage";

const EntryPage = () => {
    const router = useRouter();
    const lang = router.query.lang as string;
    const word = router.query.word?.toString();

    return (
        <BasicLayout title={word ? `${word} | OpenDictionary` : "OpenDictionary"}>
            <nav className="navbar bg-base-100 border-b-2 gap-2">
                <Link href="/">
                    <a className="btn btn-ghost normal-case text-xl" ><Logo /></a>
                </Link>
                <div className="flex-1" />
                <Link href={`/${lang}`}>
                    <a className="btn btn-ghost normal-case">Explore</a>
                </Link>
                <SelectLanguage className="" onSelect={(newLang) => router.push(`/${newLang}/${word}`)} />
            </nav>
            <main className="px-8 mx-auto max-w-screen-md py-16 min-h-[80vh]">
                <h1 className="text-4xl font-bold">{word}</h1>

                <section className="py-4">
                    <h2 className="text-xl pb-2">No results found for {`"${word}"`}.</h2>
                    <p className="text-stone-500"> Would you like to create an entry?{" "}
                        <a className="btn-link text-blue-500" href="mailto:jesse@jessehoogland.com">Reach out.</a></p>
                </section>
            </main>
        </BasicLayout>
    );
}

export default EntryPage