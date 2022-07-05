
import { createSSGHelpers } from '@trpc/react/ssg';
import { Language } from "@prisma/client";
import { GetStaticProps, GetStaticPropsContext, InferGetStaticPropsType } from "next";
import Link from "next/link";
import { useRouter } from "next/router";
import BasicLayout from "../../components/BasicLayout";
import Logo from "../../components/Logo";
import SearchBar from "../../components/SearchBar";
import SelectLanguage from "../../components/SelectLanguage";
import { appRouter } from "../../server/router";
import { trpc } from "../../utils/trpc";
import superjson from "superjson"
import groupBy from "lodash/groupBy";
import NavBar from '../../components/NavBar';

const getIPA = ({ broad, narrow }: { broad: string, narrow: string }) => broad ? `/${broad}/` : `[${narrow}]`

const EntryPage = (props: InferGetStaticPropsType<typeof getStaticProps>) => {
    const { language, word } = props;
    const entryQuery = trpc.useQuery(['entry.get', { language, word }]);
    const pronunciationQuery = trpc.useQuery(['pronunciation.listByWord', { language, word }]);
    const definitionQuery = trpc.useQuery(['definition.listByWord', { language, word }]);

    const router = useRouter();

    console.log([entryQuery, pronunciationQuery, definitionQuery])
    const doesNotExist = entryQuery.isFetched && !entryQuery.data;

    const pronunciation = groupBy(entryQuery.data ?? [], 'partOfSpeech');

    return (
        <BasicLayout title={word ? `${word} | OpenDictionary` : "OpenDictionary"}>
            <NavBar />
            <main className="px-8 mx-auto max-w-screen-md py-16 min-h-[80vh]">
                <h1 className="text-6xl font-bold">{word ?? <div className="h-10 w-[200px] animate-pulse bg-base-300 rounded-xl"></div>}</h1>

                {doesNotExist ?
                    <section className="py-4">
                        <h2 className="text-xl pb-2">No results found for {`"${word}"`}.</h2>
                        <p className="text-stone-500"> Would you like to create an entry?{" "}
                            <a className="btn-link text-blue-500" href="mailto:jesse@jessehoogland.com">Reach out.</a></p>
                    </section>
                    : <>
                        <section className='py-4 w-full'>
                            <h2 className="text-xl pb-2 font-bold">Definition</h2>
                            <div className="bg-base-200 rounded-xl p-4 prose w-full !mr-0">
                                <ul>
                                    {
                                        (definitionQuery.data ?? []).map(({ definitions }, i) => (
                                            <li key={i}>{definitions.map((def, i) => <p key={i}>{def.sentence}</p>)}</li>

                                        ))
                                    }
                                </ul>
                            </div>
                        </section>
                        <section className='py-4'>
                            <h2 className="text-xl pb-2 font-bold">Pronunciation</h2>

                            <div className="bg-base-200 rounded-xl p-4 gap-2 w-full max-w-[65ch]">
                                {
                                    (pronunciationQuery.data ?? []).map(({ broad, narrow, description }, i) => (
                                        (broad || narrow) && <span className="badge badge-outline mx-2" key={i}>{getIPA({ broad, narrow })}</span>
                                    ))
                                }
                            </div>
                        </section>
                    </>
                }


            </main>
        </BasicLayout>
    );
}

export default EntryPage


export async function getStaticProps({ params, ...ctx }: GetStaticPropsContext<{ word: string, language: Language }>) {
    const { language, word: _word } = params!;
    const word = _word.toString();

    const ssg = await createSSGHelpers({
        router: appRouter,
        ctx: {},
        transformer: superjson, // optional - adds superjson serialization
    });

    try {
        await ssg.fetchQuery('entry.get', {
            language,
            word
        })
        await ssg.fetchQuery('definition.listByWord', { language, word })
        await ssg.fetchQuery('pronunciation.listByWord', { language, word })
    } catch (e) {
        console.error(e)
    }

    return {
        props: {
            trpcState: ssg.dehydrate(),
            language,
            word,
        },
        revalidate: 1
    }

}

export async function getStaticPaths() {
    return {
        paths: [],
        fallback: true // false or 'blocking'
    };
}