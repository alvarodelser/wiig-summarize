# wiig-summarize/api/models.py
from pydantic import BaseModel


class SummarizeRequest(BaseModel):
    request_id: str | None = None
    profile:    str                 # see nlp/summarizer/profiles.py
    fields:     dict                # profile-specific; validated by the profile/prompt


class SummarizeResponse(BaseModel):
    request_id: str | None = None
    result:     dict                # e.g. {"headline","summary"} or {"description"}
