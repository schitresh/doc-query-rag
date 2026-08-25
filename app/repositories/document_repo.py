import typing as t

from psycopg2.extensions import connection


def save_document_chunks(
    connection: connection,
    document_name: str,
    chunks: list[str],
    embeddings: list[list[float]],
    embedding_model: str,
):
    """Inserts a batch of text chunks and their embeddings into PostgreSQL."""
    query = """
        INSERT INTO document_chunks (document_name, chunk_text, embedding, embedding_model)
        VALUES (%s, %s, %s, %s)
    """

    with connection:
        with connection.cursor() as cursor:
            records = []
            for chunk, embedding in zip(chunks, embeddings):
                records.append((document_name, chunk, embedding, embedding_model))

            cursor.executemany(query, records)

    return len(records)


def search_similar_chunks(
    connection: connection, query_embedding: list[float], top_k: int = 5
) -> list[dict[str, t.Any]]:
    """Performs cosine distance search to retrieve the top_k relevant chunks."""
    query = """
        SELECT id, document_name, chunk_text, (embedding <=> %s::vector) as distance
        FROM document_chunks
        ORDER BY distance ASC
        LIMIT %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (query_embedding, top_k))
        rows = cursor.fetchall()
        results = []

        for row in rows:
            results.append(
                {
                    "id": row[0],
                    "document_name": row[1],
                    "chunk_text": row[2],
                    "score": round(1 - float(row[3]), 4),
                }
            )

        return results
