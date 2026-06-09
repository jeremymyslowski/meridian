from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meridian_api.logging_config import setup_logging
from meridian_api.middleware import RequestIDMiddleware
from meridian_api.routers import (
    analytics,
    attachments,
    auth,
    comments,
    feature_flags,
    projects,
    tasks,
    teams,
    webhooks,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title="Meridian API",
    description="Team collaboration platform API",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
app.include_router(attachments.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")
app.include_router(feature_flags.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}