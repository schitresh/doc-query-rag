import typing as t

from sqlalchemy.orm import Session

from app.documents.models import DocumentChunk


def search_similar_chunks(
    db: Session, query_vector: list[float], top_k: int = 5
) -> list[dict[str, t.Any]]:
    distance_expr = DocumentChunk.embedding.cosine_distance(query_vector).label("distance")
    rows = db.query(DocumentChunk, distance_expr).order_by(distance_expr).limit(top_k).all()

    results = []
    for chunk, distance in rows:
        results.append(
            {
                "document_name": chunk.document_name,
                "chunk_text": chunk.chunk_text,
                "score": round(1 - float(distance), 4),
            }
        )

    return results
