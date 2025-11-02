# app/schemas.py

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, constr

# -----------------------
# Patient Schemas
# -----------------------

class PatientBase(BaseModel):
    identifier: constr(max_length=128)
    given_name: constr(max_length=128)
    family_name: constr(max_length=128)
    birth_date: date
    gender: Optional[constr(max_length=32)] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    identifier: Optional[constr(max_length=128)] = None
    given_name: Optional[constr(max_length=128)] = None
    family_name: Optional[constr(max_length=128)] = None
    birth_date: Optional[date] = None
    gender: Optional[constr(max_length=32)] = None

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True  # Pydantic v1


# -----------------------
# Encounter Schemas
# -----------------------

class EncounterBase(BaseModel):
    start: datetime
    end: Optional[datetime] = None
    encounter_class: constr(max_length=64)

class EncounterCreate(EncounterBase):
    patient_id: int

class EncounterUpdate(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    encounter_class: Optional[constr(max_length=64)] = None
    patient_id: Optional[int] = None  # allow reassignment if needed

class Encounter(EncounterBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True  # Pydantic v1
