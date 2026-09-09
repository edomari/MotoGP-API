"""Gateways API (`/motogp/v1/*-gateway`) — live timing and rider comparisons."""

from typing import Any

from fastapi import APIRouter, Query

from app.client import proxy_get

router = APIRouter(prefix="/motogp/v1", tags=["Gateways API"])


@router.get(
    "/timing-gateway/livetiming-lite",
    summary="Live Timing",
    description="Retrieve a timing feed during live sessions.",
    response_description="Real-time timing data (format varies depending on the session).",
)
async def get_live_timing() -> Any:
    return await proxy_get("/motogp/v1/timing-gateway/livetiming-lite")


@router.get(
    "/sportsdata-gateway/riders/pulse/statistics/comparison",
    summary="Get Comparison between Two Riders",
    description=(
        "Retrieve a statistical comparison between two specific riders for "
        "a given season, including both career and season-specific "
        "statistics."
    ),
    response_description="Comparative statistics for the two riders, indexed by UUID.",
)
async def get_riders_comparison(
    season: int = Query(..., description="The season year (e.g. `2026`).", examples=[2026]),
    rider_id1: str = Query(..., description="UUID of the first rider."),
    rider_id2: str = Query(..., description="UUID of the second rider."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/sportsdata-gateway/riders/pulse/statistics/comparison",
        {"season": season, "rider_id1": rider_id1, "rider_id2": rider_id2},
    )
