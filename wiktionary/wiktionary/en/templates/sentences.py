from wiktionary.en.templates.base import (_LANG, COMMON_IGNORE, COMMON_RENAME,
                                          TemplateMapping)

UsageExample = TemplateMapping(
    name="example",
    template_names=["ux", "eg", "uxi"],
    rename={
        "1": _LANG[1],
        "2": "value",
        "3": "gloss",
        "4": "transliteration",
        "footer": "footer",
        "ref" : "ref",
        "subst": "subst",  # So the transliteration reflects an incorrect pronunciation 
        **COMMON_RENAME
    },
    variadic_name="qualifiers",
    variadic_start="5",
    variadic_rename={"q": "q"},
    extra_transform={"qualifiers": lambda qualifiers: [q["q"] for q in qualifiers]},
    ignore=("inline", "noenum", "nocat", "sort")
)

Quote = UsageExample.copy(
    template_names=["quote", "q"],
    extra={
        "subtype": "quote",
    }
)

SourcedQuote = Quote.copy(
    template_names=["blockquote", "sourced-quote", "sourcedq"],
    rename={
        "1": "text",
        "2": "author",
        "3": "title"
    }
)

CREATOR_RENAMES = {
    "1": "langs",
    "author": "author",
    "last": "last",
    "first": "first",
    "authorlink": "authorUrl",
    "coauthors": "coauthors",
    "title": "title",
    "trans-title": "transTitle",
    "url": "url",
    "urls": "urls", # In brackets
    "archiveurl": "archiveUrl",
    "archivedate": "archiveDate",
    "accessdate": "accessDate",
    "accessmonth": "accessMonth",
    "accessyear": "accessYear",
    "format": "format",
    "publisher": "publisher",
    "year": "year",
    "month": "month",
    "day": "day",
    "date": "date",
    "yearPublished": "yearPublished",
    "location": "location",        
    "city": "city",
    "text": "text",
    "passage": "passage",
    "worklang": "workLang",
    "termlang": "termLang",
    "t": "gloss",
    "translation": "gloss",
    "footer": "footer",
    "subst": "subst",  # So the transliteration reflects an incorrect pronunciation 
}

WRITTEN_RENAMES = {
    "quotee": "quotee",
    "line": "line",
    "lines": "lines", # Separated with en dash
    "page": "page",
    "pages": "pages", # Separated with en dash
    "pageurl": "pageUrl",
    "column": "column",
    "columns": "columns", # Separated with en dash
    "columnurl": "columnUrl",
    "isbn": "isbn",
    "issn": "issn",
    "lccn": "lccn",
    "oclc": "oclc",
    "id": "id",

}


# TODO: Convert this nightmare into a reasonable, standard BibJSON
BookQuote = Quote.copy(
    template_names=["quote-book"],
    rename={  
        **COMMON_RENAME,
        **CREATOR_RENAMES, 
        **WRITTEN_RENAMES,
        "mainauthor": "mainauthor",
        "trans": "translator",
        "translator": "translator",
        "translators": "translator",
        "editors": "editors",
        "editor": "editor",
        "chapter": "chapter",
        "entry": "entry",
        "trans-chapter": "transChapter",
        "trans-entry": "transEntry",
        "chapterurl": "chapterUrl",
        "entryurl": "entryUrl",
        "series": "series",
        "seriesvolume": "seriesVolume",
        "genre": "genre",
        "edition": "edition",
        "origdate": "origDate",
        "origyear": "origYear",
        "origmonth": "origMonth",
        "volume": "volume",
        "volumeplain": "volumePlain",
        "issue": "issue",
        "number": "number",
        "section": "section",
        "sectionurl": "sectionUrl",
        "doi": "doi",
        "jstor": "jstor",
        "pmid": "pmid",
        "ol": "ol",
        "type": "type",
        "original": "original",
        "by": "by",
        "quotedIn": "quotedIn",
        # New version
        "newversion": "newVersion",
        "2ndauthor": "secondAuthor",
        "2ndlast": "secondLast",
        "2ndfirst": "secondFirst",
        "2ndauthorlink": "secondAuthorlink",
    },
    extra_transform={
        "langs": lambda langs: langs.split(","),
        "coauthors": lambda coauthors: coauthors.split(";"),
        "translators": lambda translators: translators.split(";"),
        "editors": lambda editors: editors.split(";"),
    },
    ignore=(*COMMON_IGNORE, "brackets", "indent"),
    extra={
        "subtype": "quote",
        "source": "book",
    }
)

AVQuote = BookQuote.copy(
    template_names=["quote-av"],
    rename={
        "director": "director",
        "directors": "directors",
        "actor": "actor",
        "role": "role",
        "roles": "roles",
        "speaker": "speaker",
        "episode": "episode",
        "trans-episode": "transEpisode",
        "medium": "medium",
        "season": "season",
        "number": "episode_number",
        "network": "network",
        "time": "time",
        "at": "at",
        **CREATOR_RENAMES,
        **COMMON_RENAME,
    },
    extra={
        "subtype": "quote",
        "source": "av",
    }
)

HansardQuote = BookQuote.copy(
    template_names=["quote-hansard"],
    renames={
        "speaker": "speaker",
        "report": "report",
        "house": "house",
        **WRITTEN_RENAMES,
        **CREATOR_RENAMES,
        **COMMON_RENAME
    },
    extra={
        "subtype": "quote",
        "source": "hansard",
    }
)

AVCite = AVQuote.copy(
    name="cite",
    template_names=["cite-av"],
    rename={
        **AVQuote.rename,
        "text_block": "textBlock",
        "passage_block": "textBlockUrl",
    }
)

SENTENCE_TEMPLATES = [
    Quote,
    UsageExample,
    SourcedQuote,
    BookQuote,
    AVQuote,
    HansardQuote
    # TODO: Support for quote-mailing_list, quote-newsgroup, quote-song, quote-us-patent, quote-video game, quote-wikipedia
]
