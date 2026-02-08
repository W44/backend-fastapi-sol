from sqlmodel import SQLModel

# Importing ALL models so Alembic can find them
from app.models.seashell import Seashell

# Exporting for Alembic
__all__ = ["SQLModel", "Seashell"]