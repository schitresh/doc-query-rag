import typing as t

from app.file_handler import chunker, parser


def parse_and_chunk_file(
    file: t.BinaryIO, filename: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> list[str]:
    """
    Parses text from the given file and chunks it for better processing.

    The text is splitted into small segments or chunks, and each chunk keeps some portion
    of trailing text for overlap. Chunk overlap helps keep the semantic context and preserve
    the context continuity across boundaries. Without overlap, vector search may miss
    relevant queries.
    """

    raw_text = parser.parse_file(file, filename)
    return chunker.chunk_text(raw_text, chunk_size, chunk_overlap)
