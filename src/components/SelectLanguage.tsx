import { LANGUAGES, LANGUAGE_NAMES } from "../server/router/constants";

interface SelectLanguageProps {
    className?: string;
    onSelect: (language: string) => void;
}

const SelectLanguage: React.FC<SelectLanguageProps> = ({ onSelect, className }) => (
    <select className={"select select-ghost " + (className ?? "")} onChange={(e) => onSelect(e.target.value)}>
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