import typing as t

from frontend.api_client import api_client


def fetch_folders() -> list[dict[str, t.Any]]:
    return api_client.get("folders")


def create_folder(name: str) -> dict[str, t.Any]:
    return api_client.post("/folders", params={"name": name})
