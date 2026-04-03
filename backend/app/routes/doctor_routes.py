from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models import (
    Appointment,
    AppointmentCreate,
    AppointmentPublic,
    Doctor,
    DoctorPublic,
    User,
)
from .user_routes import get_current_user

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


@router.post("/appointments", response_model=AppointmentPublic)
def create_appointment(
    *,
    session: Session = Depends(get_session),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(get_current_user),
):
    doctor = session.get(Doctor, appointment_in.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    customer = session.get(User, current_user.id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    print(appointment_in)
    # db_appointment = Appointment.model_validate(appointment_in)

    # session.add(db_appointment)
    # session.commit()
    # session.refresh(db_appointment)

    # return db_appointment


@router.get("/appointments", response_model=List[AppointmentPublic])
def read_appointments(
    *,
    session: Session = Depends(get_session),
    doctor_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    statement = select(Appointment).where(Appointment.customer_id == current_user.id)

    if doctor_id:
        statement = statement.where(Appointment.doctor_id == doctor_id)

    appointments = session.exec(statement).all()
    return appointments


# @router.get("/appointments", response_model=List[AppointmentPublic])
# def read_appointments(
#     *,
#     session: Session = Depends(get_session),
#     doctor_id: Optional[int] = None,
#     customer_id: Optional[int] = None,
#     offset: int = 0,
#     limit: int = Query(default=100, le=100),
# ):
#     statement = select(Appointment).offset(offset).limit(limit)

#     if doctor_id:
#         statement = statement.where(Appointment.doctor_id == doctor_id)
#     if customer_id:
#         statement = statement.where(Appointment.customer_id == customer_id)

#     appointments = session.exec(statement).all()
#     return appointments


# 3. Get a Single Appointment (with Doctor details)
# @router.get("/appointments/{appointment_id}", response_model=AppointmentPublic)
# def read_appointment(appointment_id: int, session: Session = Depends(get_session)):
#     appointment = session.get(Appointment, appointment_id)
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")
#     return appointment


# 4. Update Appointment (Change status, date, or time)
# @router.patch("/appointments/{appointment_id}", response_model=AppointmentPublic)
# def update_appointment(
#     appointment_id: int,
#     appointment_data: AppointmentUpdate,
#     session: Session = Depends(get_session),
# ):
#     db_appointment = session.get(Appointment, appointment_id)
#     if not db_appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")

#     # Only update fields that were actually provided in the request
#     data_dict = appointment_data.model_dump(exclude_unset=True)
#     for key, value in data_dict.items():
#         setattr(db_appointment, key, value)

#     session.add(db_appointment)
#     session.commit()
#     session.refresh(db_appointment)
#     return db_appointment


# 5. Cancel/Delete Appointment
# @router.delete("/appointments/{appointment_id}")
# def delete_appointment(appointment_id: int, session: Session = Depends(get_session)):
#     appointment = session.get(Appointment, appointment_id)
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")

#     session.delete(appointment)
#     session.commit()
#     return {"ok": True}
