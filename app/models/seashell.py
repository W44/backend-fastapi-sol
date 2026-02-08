from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Seashell(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    species: str
    description: Optional[str] = None
    deleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
