from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..models import Doctor, DoctorPublic

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("", response_model=List[DoctorPublic])
def read_doctors(
    *,
    session: Session = Depends(get_session),
    specialization: Optional[str] = None,
):
    """
    Retrieve doctors. Use 'specialization' to filter.
    """
    statement = select(Doctor)

    if specialization:
        statement = statement.where(Doctor.specialization == specialization)

    doctors = session.exec(statement).all()
    return doctors


@router.get("/{doctor_id}", response_model=DoctorPublic)
def read_doctor(doctor_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific doctor by ID, including their appointments.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
