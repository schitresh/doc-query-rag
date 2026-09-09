import typing as t

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import llm_settings
from app.database import get_db
from app.documents import repo
from app.documents.schemas import DocumentResponse, DocumentUploadResponse
from app.file_handler.processor import parse_and_chunk_file
from app.rag.embedding_generator import generate_embedding_batch

router = APIRouter(prefix="/documents", tags=["Documents"])

DatabaseDependency = t.Annotated[Session, Depends(get_db)]


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: t.Annotated[UploadFile, File(...)], folder_id: int | None, db: DatabaseDependency = None
):
    try:
        chunks = parse_and_chunk_file(file=file.file, filename=file.filename)
        if not chunks:
            raise HTTPException(status_code=400, detail="Document has no extractable text.")

        doc = repo.save_document(db, file.filename, folder_id)

        embeddings = generate_embedding_batch(chunks)
        repo.save_chunks(db, doc.id, chunks, embeddings, llm_settings.gemini_embedding_model)

        return DocumentUploadResponse(status="success", filename=file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    # except Exception:
    #     raise HTTPException(status_code=500, detail="Processing failed") from None


@router.get("/list", response_model=list[DocumentResponse])
async def list_documents(folder_id: int | None, db: DatabaseDependency = None):
    return repo.list_documents(db, folder_id)
