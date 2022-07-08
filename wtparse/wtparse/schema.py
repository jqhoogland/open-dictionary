from pydantic import BaseModel


class PronunciationEntry(BaseModel):
    pass


class WiktionaryEntry(BaseModel):
    pronunciation: list[PronunciationEntry]
