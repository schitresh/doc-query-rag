import typing as t

from google import genai

from app.config import llm_settings

GEMINI_MODEL = llm_settings.gemini_model

client = genai.Client(api_key=llm_settings.gemini_api_key)


def generate_answer(question: str, retrieved_chunks: list[dict[str, t.Any]]) -> str:
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
    prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=prompt, config={"system_instruction": system_instruction}
    )
    return response.text
