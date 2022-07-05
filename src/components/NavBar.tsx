import { Language } from "@prisma/client";
import Link from "next/link";
import router, { useRouter } from "next/router";
import Logo from "./Logo";
import SearchBar from "./SearchBar";

const NavBar: React.FC = ({ }) => {
    const { query } = useRouter();
    const { word, language } = query;

    return (
        <nav className="navbar bg-base-100 border-b-2 gap-2">
            <Link href="/">
                <a className="btn btn-ghost normal-case text-xl" ><Logo /></a>
            </Link>
            {language ? <SearchBar onSelectLanguage={(newLang) => router.push(word ? `/${newLang}/${word}` : `/${newLang}`)} className="w-full" defaultValue={language} /> : <div className='flex flex-1'></div>}
            <Link href={`/${language}`}>
                <a className="btn btn-ghost normal-case">Explore</a>
            </Link>
        </nav>
    )
}

export default NavBar;