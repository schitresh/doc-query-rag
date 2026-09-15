import typing as t

from frontend.api_client import api_client


def submit_query(question: str, folder_id: int | None = None) -> dict[str, t.Any]:
    payload = {"question": question, "folder_id": folder_id}
    return api_client.post("/rag/query", json=payload)
