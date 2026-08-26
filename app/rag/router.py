import typing as t

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.rag.content_generator import generate_answer
from app.rag.embedding_generator import generate_embedding
from app.rag.repo import search_similar_chunks
from app.rag.schemas import QueryRequest, QueryResponse

router = APIRouter(prefix="/rag", tags=["Rag"])

DatabaseDependency = t.Annotated[Session, Depends(get_db)]


@router.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest, db: DatabaseDependency = None):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question string is empty")

    query_vector = generate_embedding(payload.question)
    matching_chunks = search_similar_chunks(db, query_vector, top_k=payload.top_k)

    sources = []
    for chunk in matching_chunks:
        sources.append(
            {
                "document_name": chunk["document_name"],
                "snippet": chunk["chunk_text"][:100] + "...",
                "score": chunk["score"],
            }
        )

    answer = generate_answer(payload.question, matching_chunks)
    return {"question": payload.question, "answer": answer, "sources": sources}
