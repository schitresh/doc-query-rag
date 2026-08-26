import os
import typing as t

from pypdf import PdfReader


def parse_file(file: t.BinaryIO, filename: str) -> str:
    _, ext = os.path.splitext(filename.lower())
    parser = PARSERS.get(ext)
    if not parser:
        raise ValueError(f"Unsupported file type: {ext}")

    return parser(file)


def parse_text(file: t.BinaryIO) -> str:
    content = file.read()
    if isinstance(content, bytes):
        return content.decode("utf-8", errors="ignore")
    return content


def parse_pdf(file: t.BinaryIO) -> str:
    """Extracts raw text content from an open PDF file stream."""
    reader = PdfReader(file)
    text_pages = []

    # Iterate over the pdf pages to extract text
    for page in reader.pages:
        text = page.extract_text()

        if text:
            text_pages.append(text)

    # Join the pages using line breaks to get the raw text
    return "\n".join(text_pages)


PARSERS = {".txt": parse_text, ".md": parse_text, ".pdf": parse_pdf}
