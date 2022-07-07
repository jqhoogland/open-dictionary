import { Language } from "@prisma/client";
import { LANGUAGES, LANGUAGE_NAMES } from "../utils/constants";

interface SelectLanguageProps {
    className?: string;
    onSelect: (language: Language) => void;
    defaultValue?: Language
}

const SelectLanguage: React.FC<SelectLanguageProps> = ({ onSelect, className, ...props }) => (
    <select className={"select select-ghost " + (className ?? "")} onChange={(e) => onSelect(e.target.value as Language)} {...props}>
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
)

export default SelectLanguage;