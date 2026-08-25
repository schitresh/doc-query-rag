from google import genai

from app.config import LlmSettings

CLIENT = genai.Client(api_key=LlmSettings.gemini_api_key)
EMBEDDING_MODEL = LlmSettings.gemini_embedding_model


def generate_embedding_batch(chunks: list[str]) -> list[list[float]]:
    """Generates vector embeddings for a list of text chunks."""
    return [generate_embedding(chunk) for chunk in chunks]


def generate_embedding(chunk):
    """Generates a 768-dimensional vector embedding for a single text string."""
    response = CLIENT.models.embed_content(model=EMBEDDING_MODEL, contents=chunk)
    return response.embeddings[0].values
