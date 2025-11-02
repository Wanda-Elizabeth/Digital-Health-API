# Pydantic models for request validation and response serialization

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

# ------Patient Schemas------

class PatientBase(BaseModel):
    identifier: str = Field(..., max_length=128)
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)
    date_of_birth: Optional[date] = None

    class PatientResponse(PatientBase);
    patient_id: int = Field(..., alias="id")


    class EncounterResponse(EncounterBase):
        id: int
        patient_id: int

        class Config:
            orm_mode = True