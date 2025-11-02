# app/routes/patients.py

from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal
from app.models import Patient as PatientModel
from app.schemas import Patient, PatientCreate, PatientUpdate

router = APIRouter()

# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# NOTE: In main.py you should include this router as:
# app.include_router(patients_router, prefix="/api/patients", tags=["patients"])
# So all paths below are relative (no extra "/patients" here).

# --- Create ---
@router.post("", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    # Optional: enforce unique identifier at API level (DB unique index is recommended too)
    if payload.identifier:
        existing = (
            db.query(PatientModel)
            .filter(PatientModel.identifier == payload.identifier)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Patient with identifier '{payload.identifier}' already exists",
            )

    db_patient = PatientModel(**payload.dict(exclude_unset=True))
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# --- Read one ---
@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return patient

# --- Search / list ---
@router.get("", response_model=List[Patient])
def search_patients(
    family: Optional[str] = None,
    given: Optional[str] = None,
    identifier: Optional[str] = None,
    birthDate: Optional[date] = None,       # exact match (per brief)
    birthDateFrom: Optional[date] = None,   # range lower bound
    birthDateTo: Optional[date] = None,     # range upper bound
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    q = db.query(PatientModel)

    if family:
        q = q.filter(PatientModel.family_name.ilike(f"%{family}%"))
    if given:
        q = q.filter(PatientModel.given_name.ilike(f"%{given}%"))
    if identifier:
        q = q.filter(PatientModel.identifier.ilike(f"%{identifier}%"))
    if birthDate:
        q = q.filter(PatientModel.birth_date == birthDate)
    if birthDateFrom:
        q = q.filter(PatientModel.birth_date >= birthDateFrom)
    if birthDateTo:
        q = q.filter(PatientModel.birth_date <= birthDateTo)

    return (
        q.order_by(PatientModel.family_name, PatientModel.given_name)
         .offset(skip)
         .limit(limit)
         .all()
    )

# --- Update (full or partial, depending on your schema) ---
@router.put("/{patient_id}", response_model=Patient)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,  # define fields as Optional[...] in PatientUpdate
    db: Session = Depends(get_db),
):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # If identifier is changing, enforce uniqueness
    data = payload.dict(exclude_unset=True)
    new_identifier = data.get("identifier")
    if new_identifier and new_identifier != patient.identifier:
        exists = db.query(PatientModel).filter(PatientModel.identifier == new_identifier).first()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Patient with identifier '{new_identifier}' already exists",
            )

    for field, value in data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

# --- Delete ---
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return None


