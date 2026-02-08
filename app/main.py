from fastapi import FastAPI
from contextlib import asynccontextmanager
import os

from app.api import seashells
from app.db.session import init_db
from app.core.logging_config import setup_logging, get_logger
from app.core.middleware import log_requests

# Setup logging
log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(log_level=log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting up Seashell API")
    init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down Seashell API")


# Create the app
app = FastAPI(title="Seashell Collection API", lifespan=lifespan)

# Add middleware
app.middleware("http")(log_requests)

# Include routes
app.include_router(seashells.router, prefix="/seashells", tags=["Seashells"])


@app.get("/health")
def health_check():
    """Health check for monitoring"""
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Seashell API is running"}