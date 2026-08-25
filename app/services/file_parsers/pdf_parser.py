import typing as t

from pypdf import PdfReader


def extract_text(file: t.BinaryIO) -> str:
    """Extracts raw text content from an open PDF file stream."""
    reader = PdfReader(file)
    text_pages = []

    # Iterate over the pdf pages to extract text
    for page in reader.pages:
        text = page.extract_text()

        if text:
            text_pages.append(text)

    # Join the pages using paragraph breaks to get the raw text
    return "\n\n".join(text_pages)
