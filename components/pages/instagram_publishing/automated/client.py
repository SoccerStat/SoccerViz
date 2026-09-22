"""HTTP client of the SoccerAutomated service (see SoccerAutomated/api/server.py)."""
from typing import Optional

import requests

from config import AUTOMATED_API_URL

TIMEOUT = 15


class ApiError(Exception):
    pass


def _call(method: str, path: str, **kwargs):
    try:
        response = requests.request(method, f"{AUTOMATED_API_URL}{path}", timeout=TIMEOUT, **kwargs)
    except requests.RequestException as e:
        raise ApiError(f"Service SoccerAutomated injoignable ({AUTOMATED_API_URL}) : {e}") from e
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise ApiError(detail)
    return response


def health() -> Optional[dict]:
    try:
        return _call("GET", "/health").json()
    except ApiError:
        return None


def create_run(mode: str, text: str, chronicle: Optional[str], platforms: list[str]) -> dict:
    payload = {"mode": mode, "text": text, "chronicle": chronicle, "platforms": platforms}
    return _call("POST", "/runs", json=payload).json()


def list_runs() -> list[dict]:
    return _call("GET", "/runs").json()


def get_run(run_id: str) -> dict:
    return _call("GET", f"/runs/{run_id}").json()


def decide(run_id: str, decision: dict) -> dict:
    return _call("POST", f"/runs/{run_id}/decision", json=decision).json()


def cancel(run_id: str) -> dict:
    return _call("POST", f"/runs/{run_id}/cancel").json()


def rendered_file(run_id: str, index: int) -> bytes:
    return _call("GET", f"/runs/{run_id}/files/{index}").content
