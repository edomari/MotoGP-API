"""Content API (`/content`) — photos, videos and promotional material."""

from typing import Any, Optional

from fastapi import APIRouter, Path, Query

from app.client import proxy_get

router = APIRouter(prefix="/content", tags=["Content API"])


@router.get(
    "/riders/photos",
    summary="Get Photos for Every Rider",
    description=(
        "Retrieve the main profile photos and associated image metadata for "
        "all riders, with an option to filter by category."
    ),
    response_description="Dictionary indexed by rider UUID with photo metadata.",
)
async def get_photos_for_every_rider(
    tag: str = Query(
        ...,
        description="The image tag used to fetch the photos (e.g. `sport-data-image:rider:main`).",
        examples=["sport-data-image:rider:main"],
    ),
    motogp_category: str = Query(
        ...,
        description="The category UUID used to filter the riders.",
        examples=["737ab122-76e1-4081-bedb-334caaa18c70"],
    ),
) -> Any:
    return await proxy_get(
        "/motogp/v1/content/riders/photos",
        {"tag": tag, "motogp_category": motogp_category},
    )


@router.get(
    "/motogp/{content_type}/{language}",
    summary="Get MotoGP Content",
    description=(
        "Retrieve various types of media (photos, videos, or promos) "
        "associated with specific entities like events, teams, riders, or "
        "seasons."
    ),
    response_description="Paginated list of media content.",
)
async def get_motogp_content(
    content_type: str = Path(
        ..., description="The type of media to retrieve. Accepted values: `PHOTO`, `VIDEO`, `PROMO`.",
        examples=["PHOTO"],
    ),
    language: str = Path(
        ..., description="The language code for the content (e.g. `en`, `it`).", examples=["en"]
    ),
    references: Optional[str] = Query(
        None,
        description=(
            "A comma-separated list of reference entities to filter by, "
            "formatted as `TYPE:UUID` (e.g. `MOTOGP_RIDER:{riderId}`)."
        ),
    ),
    referenceExpression: Optional[str] = Query(
        None,
        description='Alternative to `references`, with syntax: `("MOTOGP_RIDER:{riderId}")`.',
    ),
    tagNames: str = Query(
        ...,
        description="The specific tag used to fetch the desired content.",
        examples=["sport-data-image:rider:main"],
    ),
    sort: Optional[str] = Query(None, description="The sorting order of the results (e.g. `descending`)."),
    offset: Optional[int] = Query(None, description="The pagination offset."),
    limit: Optional[int] = Query(None, description="The maximum number of results to return."),
    detail: Optional[str] = Query(None, description="The level of detail to return (e.g. `DETAILED`)."),
) -> Any:
    return await proxy_get(
        f"/content/motogp/{content_type}/{language}",
        {
            "references": references,
            "referenceExpression": referenceExpression,
            "tagNames": tagNames,
            "sort": sort,
            "offset": offset,
            "limit": limit,
            "detail": detail,
        },
    )
