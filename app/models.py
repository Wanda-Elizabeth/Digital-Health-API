# app/models.py

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base  # declarative_base() from your database.py


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    identifier: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    given_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    family_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    gender: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # Relationship
    encounters: Mapped[List["Encounter"]] = relationship(
        "Encounter",
        back_populates="patient",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        # Composite index to speed up surname+given searches
        Index("ix_patient_name", "family_name", "given_name"),
    )


class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    encounter_class: Mapped[str] = mapped_column(String(64), nullable=False)

    # Relationship
    patient: Mapped[Patient] = relationship("Patient", back_populates="encounters")
