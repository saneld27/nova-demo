"""Nova Demo – FastAPI application entry point."""
from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings

# ── Logging ──────────────────────────────────────────────────────────────────
settings = get_settings()
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Nova Demo",
    description=(
        "Agentic AI platform for Revit automation.\n\n"
        "Authenticate with a Bearer JWT issued by Auth0 that includes the "
        "`revit-plugin` provider claim."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS – restrict in production ────────────────────────────────────────────
# In production, replace "*" with the exact origin(s) of your Revit plugin host.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(router)


@app.on_event("startup")
async def on_startup() -> None:
    logger.info("Nova Demo started (env=%s, model=%s)", settings.app_env, settings.openai_model)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    logger.info("Nova Demo shutting down")
