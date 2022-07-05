import { useRouter } from "next/router";
import React from "react";
import { LANGUAGES, LANGUAGE_NAMES } from "../server/router/constants";
import SelectLanguage from "./SelectLanguage";


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
            <SelectLanguage className="absolute !min-h-0 h-auto py-0.5 pl-4 pr-8 top-2 bottom-2 right-2" onSelect={setActiveLanguage} />
        </fieldset >
    )
}

export default SearchBar