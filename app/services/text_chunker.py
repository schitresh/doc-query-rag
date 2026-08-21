# The most natural ending will be a paragraph break, then a newline, then the end of a line,
# and lastly a space. Hence, prioritize separators accordingly.
SEPARATORS = ("\n\n", "\n", ". ", "? ", "! ", " ")


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Generic text chunker using a sliding window algorithm."""
    if chunk_size <= chunk_overlap:
        raise ValueError("chunk_overlap must be strictly smaller than chunk_size")

    chunks = []
    text_length = len(text)
    start = 0
    step = chunk_size - chunk_overlap

    while start < text_length:
        end = find_natural_end(text, start, chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start += step

    return chunks


def find_natural_end(text: str, start: int, chunk_size: int) -> int:
    """
    The target end is simply the calculated end based on start position and chunk size. Natural
    end finds the nearest boundary (like a newline or space) to preserve context and keep the
    breaks natural.
    """
    target_end = start + chunk_size
    if target_end > len(text):
        return len(text) - 1

    segment = text[start:target_end]
    # If there are no separators or if its way near the start position, then the chunks will become
    # too small and meaningless. So if that's the case, the best way is to return target end as the
    # breakpoint.
    min_search_pos = len(segment) // 2

    for separator in SEPARATORS:
        pos = segment.rfind(separator)
        if pos != -1 and pos > min_search_pos:
            return start + pos + len(separator)

    return target_end
