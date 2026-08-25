import typing as t

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from psycopg2.extensions import connection

from app.database import get_db
from app.repositories.document_repo import save_document_chunks, search_similar_chunks
from app.services.embedding_generator import generate_embedding, generate_embedding_batch
from app.services.file_processor import parse_and_chunk_file
from app.services.rag_service import generate_rag_answer

router = APIRouter(prefix="/documents", tags=["Documents"])

DatabaseDependency = t.Annotated[connection, Depends(get_db)]


@router.post("/upload")
async def upload_document(
    file: t.Annotated[UploadFile, File(...)], db: DatabaseDependency = None
) -> dict[str, t.Any]:
    try:
        chunks = parse_and_chunk_file(file=file.file, filename=file.filename)
        if not chunks:
            raise HTTPException(status_code=400, detail="Document has no extractable text.")
        embeddings = generate_embedding_batch(chunks)
        save_document_chunks(db, file.filename, chunks, embeddings)

        return {"status": "success", "filename": file.filename}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception:
        raise HTTPException(status_code=500, detail="Processing failed") from None


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
