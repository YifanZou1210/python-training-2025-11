from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas import NoteCreate, NoteResponse, NoteUpdate
from app.models import Note
from app.database import get_session
from datetime import datetime

# CRUD - Create Read Update Delete

from app.dependency import DBSession

router = APIRouter(prefix='/notes')

@router.post('/', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
# dependency injection
def create_note(
    note: NoteCreate,
    # db: Session = Depends(get_session)
    # db: Annotated[Session, Depends(get_session)]
    db: DBSession
):
    user_id = 1
    db_note = Note(
        title=note.title,
        content=note.content,
        user_id=user_id
    )
    
    db.add(db_note)
    db.commit()
    return db_note


@router.get("/", response_model=list[NoteResponse])
def list_notes(db: DBSession, limit: int = 10, offset: int = 0):
    """List all notes"""
    # For now, get all notes (will filter by user in Session 2)
    statement = select(Note).offset(offset).limit(limit)
    notes = db.exec(statement).all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: DBSession):
    """Get a specific note"""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return note

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note_update: NoteUpdate, db: DBSession):
    """Update a note"""
    db_note = db.get(Note, note_id)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    # Update fields
    update_data = note_update.model_dump(exclude_unset=True)
    
    # Update fields
    for key, value in update_data.items():
        setattr(db_note, key, value)
    
    db_note.updated_at = datetime.now()
    db.add(db_note)
    db.commit()
    
    return db_note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: DBSession):
    """Delete a note"""
    db_note = db.get(Note, note_id)
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    db.delete(db_note)
    db.commit()
    return None