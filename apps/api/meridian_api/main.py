from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meridian_api.routers import auth, comments, projects, tasks

app = FastAPI(
    title="Meridian API",
    description="Team collaboration platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}