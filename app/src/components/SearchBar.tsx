import { Language } from "@prisma/client";
import { useRouter } from "next/router";
import React from "react";
import { LANGUAGES, LANGUAGE_NAMES } from "../utils/constants";
import SelectLanguage from "./SelectLanguage";

interface SelectLanguageProps { onSelectLanguage?: (lang: Language) => void; className?: string, defaultValue?: Language }

const SearchBar: React.FC<SelectLanguageProps> = ({ onSelectLanguage, className, defaultValue }) => {
    const router = useRouter();
    const [activeLanguage, setActiveLanguage] = React.useState("en");

    const handleKeyDown = React.useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.code === "Enter") {
            e.preventDefault();
            router.push(`/${activeLanguage}/${(e.target as HTMLInputElement).value}`);
        }
    }, [])

    const handleSelectLanguage = React.useCallback((lang: Language) => {
        if (onSelectLanguage) {
            onSelectLanguage(lang);
        }
        setActiveLanguage(lang)
    }, [onSelectLanguage, setActiveLanguage])

    return (
        <fieldset className={"relative " + (className ?? "")}>
            <input type="text" placeholder="Search" className="input input-bordered w-full" onKeyDown={handleKeyDown} />
            <SelectLanguage className="absolute !min-h-0 h-auto py-0.5 pl-4 pr-8 top-2 bottom-2 right-2" onSelect={handleSelectLanguage} defaultValue={defaultValue} />
        </fieldset >
    )
}

export default SearchBar