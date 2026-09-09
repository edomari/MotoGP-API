"""Shared async HTTP client, used by all routers to forward requests to
the real MotoGP API and return the JSON as received (pass-through),
while handling upstream errors."""

from typing import Any, Optional

import httpx
from fastapi import HTTPException

from app.config import MOTOGP_BASE_URL, REQUEST_TIMEOUT

_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(base_url=MOTOGP_BASE_URL, timeout=REQUEST_TIMEOUT)
    return _client


async def close_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def proxy_get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Perform a GET request against the upstream MotoGP API and forward
    its JSON response.

    Automatically strips out parameters whose value is None, so the
    generated query string stays clean even when an optional parameter
    isn't provided by the caller.
    """
    clean_params = {k: v for k, v in (params or {}).items() if v is not None}
    client = get_client()
    try:
        response = await client.get(path, params=clean_params)
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Connection error while reaching the upstream MotoGP API: {exc}",
        ) from exc

    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"The upstream MotoGP API responded with an error: {response.text[:500]}",
        )

    try:
        return response.json()
    except ValueError:
        # Some endpoints (e.g. live timing) may not return pure JSON.
        return response.text
