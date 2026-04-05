from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import (
    Appointment,
    AppointmentCreate,
    AppointmentPublic,
    Doctor,
    User,
)
from .user_routes import get_current_user

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    # Use 201 Created for POST requests that create resources
    status_code=status.HTTP_201_CREATED,
    response_model=AppointmentPublic,
    summary="Book a new appointment",
    description="""
    Creates an appointment for the currently authenticated user.

    **Logic details:**
    * The **Customer ID** is automatically assigned from the logged-in user's session.
    * The **Visit Fee** is automatically retrieved from the Doctor's current consultation fee.
    * Validates that the specified Doctor exists before creation.
    """,
    responses={
        201: {"description": "Appointment successfully created."},
        404: {"description": "Doctor not found."},
        401: {"description": "Not authenticated."},
    },
)
def create_appointment(
    *,
    session: Session = Depends(get_session),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Creates a new appointment for the currently authenticated user.
    """
    doctor = session.get(Doctor, appointment_in.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    customer = session.get(User, current_user.id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    print(appointment_in)
    db_appointment = Appointment.model_validate(
        appointment_in,
        update={
            "customer_id": current_user.id,
            "visit_fee": doctor.consultation_fee,
        },
    )

    session.add(db_appointment)
    session.commit()
    session.refresh(db_appointment)

    return db_appointment


@router.get(
    "",
    response_model=List[AppointmentPublic],
    summary="List my appointments",
    description="Retrieve a list of appointments belonging to the authenticated user. Includes an optional filter for specific doctors.",
    responses={
        200: {"description": "List of appointments retrieved successfully."},
        401: {"description": "Not authenticated."},
    },
)
def read_appointments(
    *,
    session: Session = Depends(get_session),
    doctor_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Retrieves a list of appointments for the currently authenticated user.
    """
    statement = select(Appointment).where(Appointment.customer_id == current_user.id)

    if doctor_id:
        statement = statement.where(Appointment.doctor_id == doctor_id)

    appointments = session.exec(statement).all()
    return appointments


# @router.patch("/{appointment_id}", response_model=AppointmentPublic)
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


# @router.delete("/{appointment_id}")
# def delete_appointment(appointment_id: int, session: Session = Depends(get_session)):
#     appointment = session.get(Appointment, appointment_id)
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")

#     session.delete(appointment)
#     session.commit()
#     return {"ok": True}
