from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    status: str
    filename: str
