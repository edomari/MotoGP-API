"""Results API v1 (`/motogp/v1/results`) — sessions, classifications, standings."""

from typing import Any, Optional

from fastapi import APIRouter, Path, Query

from app.client import proxy_get

router = APIRouter(prefix="/motogp/v1/results", tags=["Results API v1"])


@router.get(
    "/seasons",
    summary="Get Seasons",
    description="Retrieve a list of MotoGP seasons.",
)
async def get_seasons() -> Any:
    return await proxy_get("/motogp/v1/results/seasons")


@router.get(
    "/events",
    summary="Get Events",
    description="Retrieve a list of MotoGP events for a given season.",
)
async def get_events(
    seasonUuid: str = Query(..., description="The season UUID."),
    isFinished: Optional[bool] = Query(None, description="Filters events by whether they are finished."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/events", {"seasonUuid": seasonUuid, "isFinished": isFinished}
    )


@router.get(
    "/categories",
    summary="Get Season's / Event's Categories",
    description=(
        "Retrieve the categories of a season (`seasonUuid`) or of an event "
        "(`eventUuid`). Pass only one of the two parameters."
    ),
)
async def get_categories(
    seasonUuid: Optional[str] = Query(None, description="The season UUID."),
    eventUuid: Optional[str] = Query(None, description="The event UUID."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/categories", {"seasonUuid": seasonUuid, "eventUuid": eventUuid}
    )


@router.get(
    "/sessions",
    summary="Get Sessions",
    description="Retrieve the sessions for a given event and category.",
)
async def get_sessions(
    eventUuid: str = Query(..., description="The event UUID."),
    categoryUuid: str = Query(..., description="The category UUID."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/sessions", {"eventUuid": eventUuid, "categoryUuid": categoryUuid}
    )


@router.get(
    "/sessions/{id}",
    summary="Get Session",
    description="Retrieve the details of a single session.",
)
async def get_session(id: str = Path(..., description="The session UUID.")) -> Any:
    return await proxy_get(f"/motogp/v1/results/sessions/{id}")


@router.get(
    "/session/{id}/classification",
    summary="Get Classification",
    description="Retrieve the classification of a session.",
)
async def get_classification(
    id: str = Path(..., description="The session UUID."),
    seasonYear: Optional[int] = Query(
        None,
        description=(
            "The season year (e.g. `2023`, `2024`). Seems to have no effect, "
            "but may possibly be used for disambiguation where required."
        ),
    ),
    test: Optional[bool] = Query(None, description="Indicates whether the session is a test session."),
) -> Any:
    return await proxy_get(
        f"/motogp/v1/results/session/{id}/classification",
        {"seasonYear": seasonYear, "test": test},
    )


@router.get(
    "/event/{eventId}/entry",
    summary="Get Entry List",
    description="Retrieve the entry list for an event and a category.",
)
async def get_entry_list(
    eventId: str = Path(..., description="The event UUID."),
    categoryUuid: str = Query(..., description="The category UUID."),
) -> Any:
    return await proxy_get(
        f"/motogp/v1/results/event/{eventId}/entry", {"categoryUuid": categoryUuid}
    )


@router.get(
    "/event/{eventId}/category/{categoryId}/grid",
    summary="Get Grid Positions",
    description="Retrieve the grid positions for an event and a category.",
)
async def get_grid_positions(
    eventId: str = Path(..., description="The event UUID."),
    categoryId: str = Path(..., description="The category UUID."),
) -> Any:
    return await proxy_get(f"/motogp/v1/results/event/{eventId}/category/{categoryId}/grid")


@router.get(
    "/standings",
    summary="Get Standings",
    description="Retrieve the overall standings for a season and category.",
)
async def get_standings(
    seasonUuid: str = Query(..., description="The season UUID."),
    categoryUuid: str = Query(..., description="The category UUID."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/standings", {"seasonUuid": seasonUuid, "categoryUuid": categoryUuid}
    )


@router.get(
    "/standings/files",
    summary="Get Standings Files",
    description="Retrieve the files (e.g. PDF) related to the overall standings.",
)
async def get_standings_files(
    seasonUuid: str = Query(..., description="The season UUID."),
    categoryUuid: str = Query(..., description="The category UUID."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/standings/files",
        {"seasonUuid": seasonUuid, "categoryUuid": categoryUuid},
    )


@router.get(
    "/standings/bmwaward",
    summary="Get Rider Qualifying Standings (BMW Award)",
    description="Retrieve the qualifying standings for the BMW Award.",
)
async def get_bmw_award_standings(
    seasonUuid: str = Query(..., description="The season UUID."),
) -> Any:
    return await proxy_get("/motogp/v1/results/standings/bmwaward", {"seasonUuid": seasonUuid})


@router.get(
    "/riders-placement",
    summary="Get All-time Most Wins",
    description="Retrieve the riders with the most all-time wins, filterable by circuit and category.",
)
async def get_riders_most_wins(
    circuitUuid: Optional[str] = Query(None, description="The circuit UUID."),
    categoryName: Optional[str] = Query(None, description="The category name."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/riders-placement",
        {"circuitUuid": circuitUuid, "categoryName": categoryName},
    )


@router.get(
    "/riders-poles",
    summary="Get All-time Poles",
    description="Retrieve the riders with the most all-time pole positions.",
)
async def get_riders_poles(
    circuitUuid: Optional[str] = Query(None, description="The circuit UUID."),
    categoryName: str = Query(..., description="The category name."),
) -> Any:
    return await proxy_get(
        "/motogp/v1/results/riders-poles",
        {"circuitUuid": circuitUuid, "categoryName": categoryName},
    )


@router.get(
    "/circuit/{circuitId}/records",
    summary="Get All-time Track Records",
    description="Retrieve the all-time records of a circuit.",
)
async def get_circuit_records(
    circuitId: str = Path(..., description="The circuit UUID."),
) -> Any:
    return await proxy_get(f"/motogp/v1/results/circuit/{circuitId}/records")
