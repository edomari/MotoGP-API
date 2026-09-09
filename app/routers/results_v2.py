"""Results API v2 (`/motogp/v2/results`) — classifications, BMW Award, standings."""

from typing import Any

from fastapi import APIRouter, Query

from app.client import proxy_get

router = APIRouter(prefix="/motogp/v2/results", tags=["Results API v2"])


@router.get(
    "/classifications",
    summary="Get Session Classification",
    description=(
        "Retrieve the final classification, session details, and lap "
        "records for a specific session."
    ),
)
async def get_session_classification(
    session: str = Query(..., description="The session UUID."),
    test: bool = Query(..., description="Indicates whether the session is a test session."),
) -> Any:
    return await proxy_get("/motogp/v2/results/classifications", {"session": session, "test": test})


@router.get(
    "/bmw-award",
    summary="Get BMW Award Results",
    description="Retrieve the BMW Award results for a given season.",
)
async def get_bmw_award_results(
    season_year: str = Query(..., description="The season year."),
) -> Any:
    return await proxy_get("/motogp/v2/results/bmw-award", {"season_year": season_year})


@router.get(
    "/world-standings",
    summary="Get Last 3 Races Info for Every Rider Based on Standings",
    description=(
        "Retrieve, for every rider in the standings, information about "
        "their last 3 races."
    ),
)
async def get_world_standings(
    season: str = Query(..., description="The season UUID."),
    category: str = Query(..., description="The category UUID."),
    type: str = Query("rider", description="The type of standings.", examples=["rider"]),
) -> Any:
    return await proxy_get(
        "/motogp/v2/results/world-standings",
        {"type": type, "season": season, "category": category},
    )


@router.get(
    "/entries",
    summary="Get Event Entry List",
    description="Retrieve the entry list for an event and a category (v2).",
)
async def get_event_entries(
    categoryId: str = Query(..., description="The category UUID."),
    eventId: str = Query(..., description="The event UUID."),
) -> Any:
    return await proxy_get(
        "/motogp/v2/results/entries", {"categoryId": categoryId, "eventId": eventId}
    )
