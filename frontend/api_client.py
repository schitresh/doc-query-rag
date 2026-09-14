from os import getenv
import typing as t

import httpx

BACKEND_URL = getenv("BACKEND_URL", "http://localhost:8000")


class ApiClient:
    def __init__(self, base_url: str = BACKEND_URL, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.Client(
            base_url=self.base_url, timeout=self.timeout, headers={"Accept": "application/json"}
        )

    def close(self):
        if self.client is not None:
            self.client.aclose()

    def request(self, method: str, path: str, **kwargs) -> t.Any:
        try:
            response = self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.json().get("detail", exc.response.text)
            raise RuntimeError(detail) from exc
        except httpx.RequestError as exc:
            raise RuntimeError("Failed to connect") from exc

    def get(self, path: str, params: dict | None = None) -> t.Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, **kwargs) -> t.Any:
        return self.request("POST", path, **kwargs)


api_client = ApiClient()
