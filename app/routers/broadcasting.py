"""Broadcasting API (`/broadcasting`) — official TV broadcasters."""

from typing import Any

from fastapi import APIRouter

from app.client import proxy_get

router = APIRouter(prefix="/broadcasting", tags=["Broadcasting API"])


@router.get(
    "/broadcasters",
    summary="Get every broadcaster based on your country",
    description=(
        "Retrieve a list of official MotoGP broadcasters available in your "
        "region. The API automatically determines the appropriate country "
        "based on the requester's IP address."
    ),
    response_description="Paginated list of TV broadcasters.",
)
async def get_broadcasters() -> Any:
    return await proxy_get("/broadcasting/broadcasters")
