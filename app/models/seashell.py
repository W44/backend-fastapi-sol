from sqlmodel import SQLModel, Field
from typing import Optional

class Seashell(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    species: str
    description: Optional[str] = None
    deleted: bool = Field(default=False)
