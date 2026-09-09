"""Core API v1 (`/motogp/v1/`) — seasons, events, riders, teams."""

from typing import Any

from fastapi import APIRouter, Path, Query

from app.client import proxy_get

router = APIRouter(prefix="/motogp/v1", tags=["Core API v1"])


@router.get(
    "/categories",
    summary="Season Categories",
    description="Retrieve all categories for a single season.",
)
async def get_season_categories(
    seasonYear: int = Query(..., description="The season year (e.g. `2023`, `2024`).", examples=[2026]),
) -> Any:
    return await proxy_get("/motogp/v1/categories", {"seasonYear": seasonYear})


@router.get(
    "/events",
    summary="Get Events",
    description="Retrieve the broadcast events for a given season.",
)
async def get_events(
    seasonYear: int = Query(..., description="The season year (e.g. `2023`, `2024`).", examples=[2026]),
) -> Any:
    return await proxy_get("/motogp/v1/events", {"seasonYear": seasonYear})


@router.get(
    "/events/{id}",
    summary="Get Event",
    description="Retrieve the details of a single event.",
)
async def get_event(id: str = Path(..., description="The event UUID.")) -> Any:
    return await proxy_get(f"/motogp/v1/events/{id}")


@router.get(
    "/riders",
    summary="Get Riders",
    description="Retrieve all riders across all categories in the current season.",
)
async def get_riders() -> Any:
    return await proxy_get("/motogp/v1/riders")


@router.get(
    "/riders/{id}",
    summary="Get Rider",
    description="Retrieve the details of a single rider.",
)
async def get_rider(id: str = Path(..., description="The rider UUID.")) -> Any:
    return await proxy_get(f"/motogp/v1/riders/{id}")


@router.get(
    "/riders/{legacyId}/stats",
    summary="Get Rider Statistics",
    description="Retrieve the aggregated career statistics of a rider.",
)
async def get_rider_stats(
    legacyId: int = Path(..., description="The rider's legacy ID."),
) -> Any:
    return await proxy_get(f"/motogp/v1/riders/{legacyId}/stats")


@router.get(
    "/riders/{legacyId}/statistics",
    summary="Get Rider Statistics by Season",
    description="Retrieve rider statistics, summarised by season.",
)
async def get_rider_statistics_by_season(
    legacyId: int = Path(..., description="The rider's legacy ID."),
) -> Any:
    return await proxy_get(f"/motogp/v1/riders/{legacyId}/statistics")


@router.get(
    "/teams",
    summary="Get Teams",
    description="Retrieve the teams for a given category and season.",
)
async def get_teams(
    categoryUuid: str = Query(..., description="The broadcast category ID."),
    seasonYear: int = Query(..., description="The season year (e.g. `2023`, `2024`).", examples=[2025]),
) -> Any:
    return await proxy_get(
        "/motogp/v1/teams", {"categoryUuid": categoryUuid, "seasonYear": seasonYear}
    )


@router.get(
    "/sessions/last",
    summary="Get Last Session",
    description=(
        "Retrieve information about the most recent or currently active "
        "session for a specific category, based on event and broadcast "
        "types."
    ),
)
async def get_last_session(
    event_type: str = Query(..., alias="event-type", description="The type of the event (e.g. `sport`)."),
    broadcast_type: str = Query(
        ..., alias="broadcast-type", description="The broadcast type of the session (e.g. `session`)."
    ),
    category: str | None = Query(None, description="The category ID (e.g. `3`)."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/sessions/last",
        {"event-type": event_type, "broadcast-type": broadcast_type, "category": category},
    )
