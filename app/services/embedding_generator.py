from google import genai

from app.config import llm_settings

CLIENT = genai.Client(api_key=llm_settings.gemini_api_key)
EMBEDDING_MODEL = llm_settings.gemini_embedding_model


def generate_embedding_batch(chunks: list[str]) -> list[list[float]]:
    """Generates vector embeddings for a list of text chunks."""
    return [generate_embedding(chunk) for chunk in chunks]


def generate_embedding(chunk):
    """Generates a 768-dimensional vector embedding for a single text string."""
    response = CLIENT.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=chunk,
        config=genai.types.EmbedContentConfig(output_dimensionality=768),
    )
    return response.embeddings[0].values
