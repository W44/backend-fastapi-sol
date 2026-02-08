from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import seashells
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    yield

app = FastAPI(title="Seashell Collection API", lifespan=lifespan)

# Include routes
app.include_router(seashells.router, prefix="/seashells", tags=["Seashells"])

@app.get("/", status_code=201)
def root():
    return "Server Connected."