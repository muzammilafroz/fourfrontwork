from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Prescription, User
from .user_routes import get_current_user

router = APIRouter(prefix="/prescription", tags=["prescription"])


@router.post("/create", response_model=Prescription)
def create_prescription(
    prescription: Prescription, session: Session = Depends(get_session)
):
    session.add(prescription)
    session.commit()
    session.refresh(prescription)
    return prescription


@router.get("/{prescription_id}", response_model=Prescription)
def read_prescription(prescription_id: int, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    return prescription


@router.get("/", response_model=List[Prescription])
def read_customer_prescriptions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Prescription).where(Prescription.customer_id == current_user)
    prescriptions = session.exec(statement).all()
    return prescriptions
