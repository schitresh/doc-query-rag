from sqlalchemy.orm import Session

from app.documents.models import DocumentChunk


def search_similar_chunks(
    db: Session, query_vector: list[float], top_k: int = 5
) -> list[DocumentChunk]:
    return (
        db.query(DocumentChunk)
        .order_by(DocumentChunk.embedding.cosine_distance(query_vector))
        .limit(top_k)
        .all()
    )
