"""Reusable REST client patterns for network APIs."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiClient:
    base_url: str
    token: str
    verify_ssl: bool = True
    timeout_seconds: int = 20
    retries: int = 3
    retry_backoff: float = 1.5

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def request(self, method: str, path: str, json_body: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        attempt = 0

        while True:
            attempt += 1
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self._headers(),
                json=json_body,
                timeout=self.timeout_seconds,
                verify=self.verify_ssl,
            )

            if response.ok:
                return response.json() if response.text else None

            if attempt >= self.retries or response.status_code not in {429, 500, 502, 503, 504}:
                raise RuntimeError(
                    f"API call failed {method} {url} status={response.status_code} body={response.text}"
                )

            sleep_for = self.retry_backoff ** attempt
            time.sleep(sleep_for)


def from_env(prefix: str) -> ApiClient:
    return ApiClient(
        base_url=os.environ[f"{prefix}_BASE_URL"],
        token=os.environ[f"{prefix}_TOKEN"],
        verify_ssl=os.getenv(f"{prefix}_VERIFY_SSL", "true").lower() == "true",
    )
