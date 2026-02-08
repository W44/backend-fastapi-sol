from pydantic import BaseModel
from typing import Optional

class SeashellCreate(BaseModel):
    name: str
    species: str
    description: Optional[str] = None

class SeashellRead(SeashellCreate):
    id: int

class SeashellUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    description: Optional[str] = None
