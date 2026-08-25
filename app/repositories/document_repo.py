from psycopg2.extensions import connection


def save_document_chunks(
    connection: connection, document_name: str, chunks: list[str], embeddings: list[list[float]]
):
    """Inserts a batch of text chunks and their embeddings into PostgreSQL."""
    query = """
        INSERT INTO document_chunks (document_name, chunk_text, embedding)
        VALUES (%s, %s, %s)
    """

    with connection:
        with connection.cursor() as cursor:
            records = []
            for chunk, embedding in zip(chunks, embeddings):
                records.append((document_name, chunk, str(embedding)))

            cursor.executemany(query, records)

    return len(records)


def search_similar_chunks(
    connection: connection, query_embedding: list[float], top_k: int = 5
) -> list[dict[str, any]]:
    """Performs cosine distance search to retrieve the top_k relevant chunks."""
    query = """
        SELECT id, document_name, chunk_text, (embedding <=> %s::vector) as distance
        FROM document_chunks
        ORDER BY distance ASC
        LIMIT %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (str(query_embedding), top_k))
        rows = cursor.fetch_all()
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
