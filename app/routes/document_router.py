import typing as t

from fastapi import APIRouter, Depends, HTTPException
from psycopg2.extensions import connection

from app.database import get_db
from app.rag_service.content_generator import generate_rag_answer
from app.rag_service.embedding_generator import generate_embedding
from app.rag_service.repo import search_similar_chunks

router = APIRouter(prefix="/documents", tags=["Documents"])

DatabaseDependency = t.Annotated[connection, Depends(get_db)]


@router.get("/search")
async def search_documents(query: str, top_k: int = 5, db: DatabaseDependency = None):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query string is empty")

    query_vector = generate_embedding(query)
    results = search_similar_chunks(db, query_vector, top_k=top_k)

    return {"query": query, "result_count": len(results), "results": results}


@router.get("/query")
async def query_documents(
    query: str, top_k: int = 5, db: DatabaseDependency = None
) -> dict[str, t.Any]:
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query string is empty")

    query_vector = generate_embedding(query)
    matching_chunks = search_similar_chunks(db, query_vector, top_k=top_k)
    answer = generate_rag_answer(query, matching_chunks)

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "document_name": chunk["document_name"],
                "score": chunk["score"],
                "snippet": chunk["chunk_text"][:100] + "...",
            }
            for chunk in matching_chunks
        ],
    }
