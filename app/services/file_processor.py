import os
import typing as t

from app.services import text_chunker
from app.services.file_parsers import pdf_parser

PARSERS = {".pdf": pdf_parser.extract_text}


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

    _, ext = os.path.splitext(filename.lower())
    parser = PARSERS.get(ext)
    if not parser:
        raise ValueError(f"Unsupported file type: {ext}")

    raw_text = parser(file)
    return text_chunker.chunk_text(raw_text, chunk_size, chunk_overlap)
