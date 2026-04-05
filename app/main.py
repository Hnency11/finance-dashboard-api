from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.routes import auth, records, summary, users
from app import models

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle FastAPI startup and shutdown events."""
    yield


app = FastAPI(
    title=settings.API_TITLE,
    description="Backend API for the Finance Dashboard",
    version="0.1.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(auth.router)
app.include_router(records.router)
app.include_router(summary.router)
app.include_router(users.router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Basic API health check."""
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Finance API running"}