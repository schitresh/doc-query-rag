from collections.abc import Generator

import psycopg2
from psycopg2.extensions import connection as PgConnection

from app.config import settings


def get_db_connection() -> PgConnection:
    """Returns a fresh raw PostgreSQL connection."""
    return psycopg2.connect(settings.db_url)


def get_db() -> Generator[PgConnection]:
    """
    FastAPI dependency yielding a connection for an HTTP request
    and ensuring closure after the response is sent.
    """
    connection = get_db_connection()
    try:
        yield connection
    finally:
        connection.close()


def create_vector_extention(connection: PgConnection) -> None:
    """Enables the pgvector extension in PostgreSQL."""
    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def create_chunks_table(connection: PgConnection) -> None:
    """Creates the document_chunks table if it does not exist."""
    query = """
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            document_name VARCHAR(255) NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding vector(768) NOT NULL,
            embedding_model VARCHAR(100) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(query)


def init_db() -> None:
    """Initialize the database setup and create chunks table"""
    connection = get_db_connection()
    with connection:
        create_vector_extention(connection)
        create_chunks_table(connection)
    connection.close()


if __name__ == "__main__":
    init_db()
