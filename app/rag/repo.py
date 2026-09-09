import typing as t

from sqlalchemy.orm import Session

from app.documents.models import Document, DocumentChunk


def search_similar_chunks(
    db: Session, query_vector: list[float], top_k: int = 5, folder_id: int | None = None
) -> list[dict[str, t.Any]]:
    distance_expr = DocumentChunk.embedding.cosine_distance(query_vector).label("distance")

    rows = db.query(Document, DocumentChunk, distance_expr).join(
        Document, DocumentChunk.document_id == Document.id
    )

    if folder_id is not None:
        rows = rows.filter(Document.folder_id == folder_id)

    rows = rows.order_by(distance_expr).limit(top_k).all()

    results = []
    for chunk, distance in rows:
        results.append(
            {
                "document_name": chunk.filename,
                "chunk_text": chunk.chunk_text,
                "score": round(1 - float(distance), 4),
            }
        )

    return results
