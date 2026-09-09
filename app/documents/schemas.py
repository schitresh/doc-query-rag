import datetime as dt

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    status: str
    filename: str


class DocumentResponse(BaseModel):
    id: int
    filename: str
    folder_id: int | None
    created_at: dt.datetime
