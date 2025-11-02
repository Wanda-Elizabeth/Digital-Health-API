# Small layer of CRUD functions so that routes remain thin and logic is testable

from sqlalchemy.orm import Session
from sqlalchemy import and_
from . imprt models, schema
from typing import List, Optional
from datetime import date


#---Patients---

def create_patient(db: Session, patient_in: schema.PatientCreate) -> models.Patient:
  db_patient = models.Patient(
    identifier=patient_in.identifier,
    first_name=patient_in.first_name,
    last_name=patient_in.last_name,
    date_of_birth=patient_in.date_of_birth,
    gender=patient_in.gender
  )
  db.add(db_patient)
  db.commit()
  db.refresh(db_patient)
  return db_patient


  def get_patient(db:Session, patient_id:int) -> Optional[models.Patient]:
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


    def update_patient(db:Session, patient_id:int, patient_in:schema.PatientUpdate) -> Optional[models.Patient]:
      db_patient = get_patient(db, patient_id)
      if not db_patient:
        return None
      for field, value in patient_in.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)
      db.commit()
      db.refresh(db_patient)
      return db_patient


      def delete_patient(db:Session, patient_id:int) -> bool:
        db_patient = get_patient(db, patient_id)
        if not db_patient:
          return False
        db.delete(db_patient)
        db.commit()
        return True

        def search_patients(db: Session,
        last_name : Optional[str] = None,
        first_name : Optional[str] = None,
        identifier : Optional[str] = None,
        date_of_birth : Optional[date] = None
        skip: int = 0,
        limit: int = 10
        ) -> List[models.Patient]:
          query = db.query(models.Patient)



          #Flexible patient search with partial matching and date range support
          #Returns a list of Patient ORM objects

            if last_name:
                query = query.filter(models.Patient.last_name.ilike(f"%{last_name}%"))
            if first_name:
                query = query.filter(models.Patient.first_name.ilike(f"%{first_name}%"))
            if identifier:
                query = query.filter(models.Patient.identifier.ilike(f"%{identifier}%"))
            if date_of_birth:
                query = query.filter(models.Patient.date_of_birth == date_of_birth)
            return query.order_by(models.Patient.last_name, models.Patient.first_name).offset(skip).limit(limit).all()


       #---Encounters---
def create_encounter(db: Session, encounter_in: schema.EncounterCreate) -> models.Encounter:
    db_encounter = models.Encounter(
        patient_id=encounter_in.patient_id,
        start=encounter_in.start,
        end=encounter_in.end,
        encounter_class=encounter_in.encounter_class
    )
    db.add(db_encounter)
    db.commit()
    db.refresh(db_encounter)
    return db_encounter

def get_encounter(db: Session, encounter_id: int) -> Optional[models.Encounter]:
    return db.query(models.Encounter).filter(models.Encounter.id == encounter_id).first()

def get_encounters_by_patient(db: Session, patient_id: int, skip: int = 0, limit: int = 10) -> List[models.Encounter]:
    return db.query(models.Encounter).filter(models.Encounter.patient_id == patient_id).order_by(models.Encounter.start.desc()).offset(skip).limit(limit).all()

