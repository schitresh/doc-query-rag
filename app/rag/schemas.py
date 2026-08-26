from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


class SourceChunk(BaseModel):
    document_name: str
    chunk_text: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
