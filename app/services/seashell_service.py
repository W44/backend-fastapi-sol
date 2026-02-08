from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException
from app.models.seashell import Seashell
from app.schemas.seashell import SeashellCreate, SeashellUpdate


class SeashellService:
    """Service layer for seashell business logic"""
    
    @staticmethod
    def create_seashell(seashell_data: SeashellCreate, session: Session) -> Seashell:
        """Create a new seashell"""
        db_seashell = Seashell.from_orm(seashell_data)
        session.add(db_seashell)
        session.commit()
        session.refresh(db_seashell)
        return db_seashell
    
    @staticmethod
    def get_seashells(
        skip: int, 
        limit: int, 
        session: Session,
        search: Optional[str] = None,
        sort_by: str = "id",
        order: str = "asc"
    ) -> List[Seashell]:
        """Get all non-deleted seashells with pagination, search, and sorting"""
        # Base query - only non-deleted items
        statement = select(Seashell).where(Seashell.deleted == False)
        
        # Apply global search across name, species, and description
        if search:
            search_filter = f"%{search}%"
            statement = statement.where(
                (Seashell.name.ilike(search_filter)) |
                (Seashell.species.ilike(search_filter)) |
                (Seashell.description.ilike(search_filter))
            )
        
        # Apply sorting
        sort_column = getattr(Seashell, sort_by, Seashell.id)
        if order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column.asc())
        
        # Apply pagination
        statement = statement.offset(skip).limit(limit)
        
        seashells = session.exec(statement).all()
        return seashells
    
    @staticmethod
    def get_seashell_by_id(seashell_id: int, session: Session) -> Seashell:
        """Get a seashell by ID, raise 404 if not found or deleted"""
        seashell = session.get(Seashell, seashell_id)
        if not seashell or seashell.deleted:
            raise HTTPException(status_code=404, detail="Seashell not found")
        return seashell
    
    @staticmethod
    def update_seashell(seashell_id: int, seashell_update: SeashellUpdate, session: Session) -> Seashell:
        """Update a seashell by ID"""
        seashell = SeashellService.get_seashell_by_id(seashell_id, session)
        
        # Update only fields that were provided
        update_data = seashell_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(seashell, key, value)
        
        session.add(seashell)
        session.commit()
        session.refresh(seashell)
        return seashell
    
    @staticmethod
    def delete_seashell(seashell_id: int, session: Session) -> None:
        """Soft delete a seashell by ID"""
        seashell = SeashellService.get_seashell_by_id(seashell_id, session)
        seashell.deleted = True
        session.add(seashell)
        session.commit()
