from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models import Doctor, DoctorCreate, DoctorPublic, DoctorUpdate

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get(
    "",
    response_model=List[DoctorPublic],
    summary="List all doctors",
)
def read_doctors(
    *,
    session: Session = Depends(get_session),
    specialization: Optional[str] = Query(None),
):
    statement = select(Doctor)
    if specialization:
        statement = statement.where(Doctor.specialization == specialization)
    doctors = session.exec(statement).all()
    return doctors


@router.get("/{doctor_id}", response_model=DoctorPublic, summary="Get a doctor by ID")
def read_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post(
    "",
    # response_model: public profile of the created doctor
    response_model=DoctorPublic,
    summary="Create a new doctor",
    description="Register a new doctor in the system with their specialization and availability.",
)
def create_doctor(*, session: Session = Depends(get_session), doctor: DoctorCreate):
    """
    Create a new doctor entry.
    """
    # Convert the DoctorCreate Pydantic model into a Doctor SQLModel table instance
    db_doctor = Doctor.model_validate(doctor)
    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor


@router.patch(
    "/{doctor_id}",
    response_model=DoctorPublic,
    summary="Update a doctor",
    description="Update specific fields of an existing doctor's profile.",
)
def update_doctor(
    *, session: Session = Depends(get_session), doctor_id: int, doctor: DoctorUpdate
):
    """
    Update an existing doctor. Only provide the fields you wish to change.
    """
    db_doctor = session.get(Doctor, doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Extract only the data provided in the request (ignore defaults)
    doctor_data = doctor.model_dump(exclude_unset=True)
    db_doctor.sqlmodel_update(doctor_data)

    session.add(db_doctor)
    session.commit()
    session.refresh(db_doctor)
    return db_doctor


@router.delete(
    "/{doctor_id}",
    summary="Delete a doctor",
    description="Permanently remove a doctor from the system.",
)
def delete_doctor(*, session: Session = Depends(get_session), doctor_id: int):
    """
    Delete a doctor record by ID.
    """
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    session.delete(doctor)
    session.commit()
    return {"ok": True}
