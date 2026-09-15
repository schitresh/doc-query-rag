import typing as t

from frontend.api_client import api_client


def fetch_documents(folder_id: int) -> list[dict[str, t.Any]]:
    params = {"folder_id": folder_id}
    return api_client.get("/documents", params=params)


def upload_document(file_bytes: bytes, filename: str, folder_id: int) -> dict[str, t.Any]:
    files = {"file": (filename, file_bytes)}
    params = {"folder_id": str(folder_id)}
    return api_client.post("/documents/upload", files=files, params=params)
