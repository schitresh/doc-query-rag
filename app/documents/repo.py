from sqlalchemy.orm import Session

from app.documents.models import DocumentChunk


def save_chunks(
    db: Session,
    document_name: str,
    chunks: list[str],
    embeddings: list[list[float]],
    embedding_model: str,
) -> int:
    chunk_objects = []
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
        chunk_objects.append(
            DocumentChunk(
                document_name=document_name,
                chunk_index=idx,
                chunk_text=chunk,
                embedding=embedding,
                embedding_model=embedding_model,
            )
        )

    db.add_all(chunk_objects)
    db.commit()
    return len(chunk_objects)
