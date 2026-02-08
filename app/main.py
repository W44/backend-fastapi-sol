from fastapi import FastAPI
from app.api import seashells
from app.db.session import init_db

app = FastAPI(title="Seashell Collection API")

# Database initialization on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Include routes
app.include_router(seashells.router, prefix="/seashells", tags=["Seashells"])

@app.get("/", status_code=201)
def root():
    return "Server Connected."