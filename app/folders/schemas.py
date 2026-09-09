import datetime as dt

from pydantic import BaseModel


class FolderCreate(BaseModel):
    id: int
    name: str


class FolderResponse(BaseModel):
    id: int
    name: str
    created_at: dt.datetime
