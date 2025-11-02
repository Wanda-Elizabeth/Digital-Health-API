# app/routes/encounters.py

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Encounter as EncounterModel
from app.schemas import Encounter, EncounterCreate, EncounterUpdate  # ensure these exist and match fields

router = APIRouter()

# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NOTE: In main.py include with:
# app.include_router(encounters_router, prefix="/api/encounters", tags=["encounters"])

# --- Create ---
@router.post("", response_model=Encounter, status_code=status.HTTP_201_CREATED)
def create_encounter(payload: EncounterCreate, db: Session = Depends(get_db)):
    db_encounter = EncounterModel(**payload.dict(exclude_unset=True))
    db.add(db_encounter)
    db.commit()
    db.refresh(db_encounter)
    return db_encounter

# --- Read one ---
@router.get("/{encounter_id}", response_model=Encounter)
def read_encounter(encounter_id: int, db: Session = Depends(get_db)):
    enc = db.query(EncounterModel).filter(EncounterModel.id == encounter_id).first()
    if not enc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encounter not found")
    return enc

# --- List / query  ---
@router.get("", response_model=List[Encounter])
def list_encounters(
    patient_id: Optional[int] = None,
    start_from: Optional[datetime] = Query(None, alias="from"),
    start_to: Optional[datetime] = Query(None, alias="to"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    q = db.query(EncounterModel)
    if patient_id is not None:
        q = q.filter(EncounterModel.patient_id == patient_id)
    if start_from is not None:
        q = q.filter(EncounterModel.start >= start_from)
    if start_to is not None:
        q = q.filter(EncounterModel.start <= start_to)

    return q.order_by(EncounterModel.start.desc()).offset(skip).limit(limit).all()

# --- Update (partial) ---
@router.put("/{encounter_id}", response_model=Encounter)
def update_encounter(
    encounter_id: int,
    payload: EncounterUpdate,
    db: Session = Depends(get_db),
):
    enc = db.query(EncounterModel).filter(EncounterModel.id == encounter_id).first()
    if not enc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encounter not found")

    data = payload.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(enc, field, value)

    db.commit()
    db.refresh(enc)
    return enc

# --- Delete ---
@router.delete("/{encounter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_encounter(encounter_id: int, db: Session = Depends(get_db)):
    enc = db.query(EncounterModel).filter(EncounterModel.id == encounter_id).first()
    if not enc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Encounter not found")
    db.delete(enc)
    db.commit()
    return None
