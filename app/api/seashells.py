from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from app.db.session import get_session
from app.schemas.seashell import SeashellCreate, SeashellRead, SeashellUpdate
from app.services.seashell_service import SeashellService

router = APIRouter()

@router.post("/", response_model=SeashellRead, status_code=201)
def create_seashell(seashell: SeashellCreate, session: Session = Depends(get_session)):
    """Create a new seashell"""
    return SeashellService.create_seashell(seashell, session)

@router.get("/", response_model=List[SeashellRead])
def list_seashells(
    page: int = Query(default=1, ge=1, description="Page number (starts at 1)"),
    page_size: int = Query(default=10, ge=1, lte=100, description="Items per page (max 100)"),
    sort_by: str = Query(default="id", pattern="^(id|name|species|description)$", description="Field to sort by"),
    order: str = Query(default="asc", pattern="^(asc|desc)$", description="Sort order"),
    search: Optional[str] = Query(default=None, description="Search across name, species, and description (case-insensitive)"),
    session: Session = Depends(get_session)
):
    """
    Get all seashells with advanced pagination, search, and sorting.
    """
    skip = (page - 1) * page_size
    return SeashellService.get_seashells(
        skip, page_size, session,
        search=search,
        sort_by=sort_by, order=order
    )

@router.get("/{seashell_id}", response_model=SeashellRead)
def get_seashell(seashell_id: int, session: Session = Depends(get_session)):
    """Get a specific seashell by ID"""
    return SeashellService.get_seashell_by_id(seashell_id, session)

@router.put("/{seashell_id}", response_model=SeashellRead)
def update_seashell(
    seashell_id: int, 
    seashell_update: SeashellUpdate, 
    session: Session = Depends(get_session)
):
    """Update a seashell by ID"""
    return SeashellService.update_seashell(seashell_id, seashell_update, session)

@router.delete("/{seashell_id}", status_code=204)
def delete_seashell(seashell_id: int, session: Session = Depends(get_session)):
    """Soft delete a seashell by ID"""
    SeashellService.delete_seashell(seashell_id, session)
