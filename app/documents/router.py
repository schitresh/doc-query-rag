import typing as t

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import llm_settings
from app.database import get_db
from app.documents.repo import save_chunks
from app.documents.schemas import DocumentUploadResponse
from app.file_handler.processor import parse_and_chunk_file
from app.rag.embedding_generator import generate_embedding_batch

router = APIRouter(prefix="/documents", tags=["Documents"])

DatabaseDependency = t.Annotated[Session, Depends(get_db)]


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: t.Annotated[UploadFile, File(...)], db: DatabaseDependency = None):
    try:
        chunks = parse_and_chunk_file(file=file.file, filename=file.filename)
        if not chunks:
            raise HTTPException(status_code=400, detail="Document has no extractable text.")

        embeddings = generate_embedding_batch(chunks)
        save_chunks(db, file.filename, chunks, embeddings, llm_settings.gemini_embedding_model)

        return DocumentUploadResponse(status="success", filename=file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception:
        raise HTTPException(status_code=500, detail="Processing failed") from None
