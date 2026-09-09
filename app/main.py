"""MotoGP API — unofficial FastAPI wrapper.

Exposes every endpoint documented in the original README.md as a proxy
towards the real MotoGP API (https://api.motogp.pulselive.com),
automatically generating a full Swagger/OpenAPI documentation.
"""

import os
import sys
from contextlib import asynccontextmanager

# Allows this file to also be run directly as a script
# (`python3 main.py` from inside app/, or `python3 app/main.py` from the
# project root), by adding the project root to sys.path so that
# `from app.client import ...` can be resolved. The recommended way to
# run the app remains `uvicorn app.main:app --reload` from the project
# root.
if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.client import close_client
from app.routers import broadcasting, content, core, gateways, results_v1, results_v2

DESCRIPTION = """
Unofficial **FastAPI** wrapper for the public MotoGP API
(`https://api.motogp.pulselive.com`).

This project is **not affiliated with Dorna Sports / MotoGP**: it
documents and forwards (proxies) calls to observed public endpoints,
for educational and reference purposes.

### Sections

- 📷 **Content API** — photos, videos and promotional material.
- 📺 **Broadcasting API** — official TV broadcasters.
- ⏱️ **Gateways API** — live timing and rider statistical comparisons.
- 🏁 **Results API v1 / v2** — sessions, classifications, grids, standings.
- 🏍️ **Core API v1** — seasons, events, riders, teams.

The API is **read-only**: only the `GET` method is exposed.
"""

tags_metadata = [
    {"name": "Content API", "description": "Photos, videos and promotional material (`/content`)."},
    {"name": "Broadcasting API", "description": "Official TV broadcasters (`/broadcasting`)."},
    {"name": "Gateways API", "description": "Live timing and statistical comparisons (`/motogp/v1/*-gateway`)."},
    {"name": "Results API v1", "description": "Sessions and classifications v1 (`/motogp/v1/results`)."},
    {"name": "Results API v2", "description": "Sessions and classifications v2 (`/motogp/v2/results`)."},
    {"name": "Core API v1", "description": "Seasons, events, riders, teams (`/motogp/v1/`)."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_client()


# Vercel automatically sets VERCEL_URL to the domain of the current
# deployment (both in production and in every PR preview). We use it so
# the OpenAPI schema (and therefore "Try it out" in Swagger UI) always
# points to the correct domain, with no manual configuration needed.
_vercel_url = os.getenv("VERCEL_URL")
API_BASE_URL = os.getenv("API_BASE_URL") or (f"https://{_vercel_url}" if _vercel_url else None)
servers = [{"url": API_BASE_URL, "description": "Live instance"}] if API_BASE_URL else None

app = FastAPI(
    title="MotoGP API (Unofficial)",
    description=DESCRIPTION,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={"name": "GitHub Repository", "url": "https://github.com/edomari/MotoGP-API"},
    license_info={"name": "MIT"},
    lifespan=lifespan,
    servers=servers,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(content.router)
app.include_router(broadcasting.router)
app.include_router(gateways.router)
app.include_router(results_v1.router)
app.include_router(results_v2.router)
app.include_router(core.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    # Also allows `python3 app/main.py`, in addition to
    # `uvicorn app.main:app --reload`.
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
