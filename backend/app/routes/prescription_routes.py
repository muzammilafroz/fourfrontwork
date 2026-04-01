from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.crud import save_base64_image
from app.llm import extract_prescription_data

from ..database import get_session
from ..models import (
    Medication,
    Prescription,
    PrescriptionCreate,
    PrescriptionPublic,
    User,
)
from .user_routes import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["prescription"])


@router.post("/create", response_model=PrescriptionPublic)
def create_prescription(
    prescription_in: PrescriptionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    img_path = save_base64_image(
        prescription_in.image_base64, upload_dir=Path("uploads/prescriptions")
    )

    try:
        prescription_data = extract_prescription_data(img_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI extraction failed: {str(e)}",
        )

    db_medications = [
        Medication(
            name=m.name, dosage=m.dosage, frequency=m.frequency, duration=m.duration
        )
        for m in prescription_data.medications
    ]

    db_prescription = Prescription(
        image_path=img_path,
        customer_id=current_user.id or 0,
        doctor_name=prescription_data.doctor_name,
        date=prescription_data.date,
        medications=db_medications,
    )

    try:
        session.add(db_prescription)
        session.commit()
        session.refresh(db_prescription)
        return db_prescription
    except Exception as e:
        session.rollback()
        print(f"Database Error: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to save prescription to database."
        )


@router.get("/{prescription_id}", response_model=PrescriptionPublic)
def read_prescription(
    prescription_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    prescription = session.get(Prescription, prescription_id)
    if prescription.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Prescription is not yours."
        )
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found."
        )
    return prescription


@router.get("", response_model=List[PrescriptionPublic])
def read_customer_prescriptions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        statement = select(Prescription).where(
            Prescription.customer_id == current_user.id
        )
        prescriptions = session.exec(statement).all()
    except Exception as e:
        prescriptions = []
        print(f"Error: {e}")

    return prescriptions
