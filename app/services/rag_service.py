from google import genai

from app.config import LlmSettings

CLIENT = genai.Client(api_key=LlmSettings.gemini_api_key)
GEMINI_MODEL = LlmSettings.gemini_model


def generate_rag_answer(query: str, retrieved_chunks: list[dict[str, any]]) -> str:
    if not retrieved_chunks:
        return "No relevant information found."

    # Format the retrieved chunks into a structured context string
    context = "\n\n---\n\n".join(
        f"[Source]: {chunk['document_name']}\n{chunk['chunk_text']}" for chunk in retrieved_chunks
    )
    # Construct system instructions to make the answer reliable and prevent outside knowledge
    system_instruction = (
        "You are an accurate assistant answering questions based strictly on provided document"
        "excerpts. "
        "Rules:\n"
        "1. Rely ONLY on the clear facts in the context below.\n"
        "2. Do NOT extrapolate, speculate, or use outside knowledge.\n"
        "3. If the answer is not contained within the context, respond with: "
        "'No relevant information found.'"
    )
    prompt = f"Context:\n{context}\n\nQuestion: {query}"

    response = CLIENT.models.generate_content(
        model=GEMINI_MODEL, contents=prompt, config={"system_instruction": system_instruction}
    )
    return response.text
