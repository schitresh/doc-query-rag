from sqlalchemy.orm import Session

from app.documents.models import Document, DocumentChunk


def save_document(db: Session, filename: str, folder_id: int | None) -> Document:
    doc = Document(filename=filename, folder_id=folder_id)
    db.add(doc)
    db.flush()

    return doc


def save_chunks(
    db: Session,
    document_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
    embedding_model: str,
) -> int:
    chunk_objects = []
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
        chunk_objects.append(
            DocumentChunk(
                document_id=document_id,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=embedding,
                embedding_model=embedding_model,
            )
        )

    db.add_all(chunk_objects)
    db.commit()
    return len(chunk_objects)


def list_documents(db: Session, folder_id: int | None) -> list[Document]:
    query = db.query(Document)

    if folder_id is not None:
        query = query.filter(Document.folder_id == folder_id)

    return query.all()
