from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models import Doctor, DoctorPublic

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get(
    "",
    response_model=List[DoctorPublic],
    summary="List all doctors",
    description="Retrieve a list of doctors from the database. You can optionally filter the results by their medical specialization.",
    response_description="A list of doctor objects containing public profile information.",
)
def read_doctors(
    *,
    session: Session = Depends(get_session),
    specialization: Optional[str] = Query(
        None,
        description="Filter doctors by their medical specialty (e.g., 'Cardiology', 'Pediatrics')",
        examples=["Cardiology", "Neurology"],
    ),
):
    """
    Retrieve doctors. Use 'specialization' to filter.
    """
    statement = select(Doctor)

    if specialization:
        statement = statement.where(Doctor.specialization == specialization)

    doctors = session.exec(statement).all()
    return doctors


@router.get(
    "/{doctor_id}",
    response_model=DoctorPublic,
    summary="Get a doctor by ID",
    description="Fetch detailed information about a specific doctor using their unique integer ID.",
    responses={
        200: {"description": "Doctor found and returned."},
        404: {"description": "No doctor exists with the provided ID."},
    },
)
def read_doctor(doctor_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a specific doctor by ID, including their appointments.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
