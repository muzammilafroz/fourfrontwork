from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.crud import save_base64_image
from app.llm import extract_prescription_data

from ..database import get_session
from ..models import Prescription, PrescriptionBase, PrescriptionCreate, User
from .user_routes import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["prescription"])


# TODO: Create a new prescription data entry.
@router.post("/create", response_model=PrescriptionBase)
def create_prescription(
    prescription: PrescriptionCreate, session: Session = Depends(get_session)
):
    # session.add(prescription)
    # session.commit()
    # session.refresh(prescription)
    # return prescription

    img_path = save_base64_image(
        prescription.image_base64, upload_dir=Path("uploads/prescriptions")
    )

    try:
        prescription_data = extract_prescription_data(img_path)
        print(prescription_data)

    except Exception as e:
        print(f"Error: {e}")

    # TODO: Parse the AI response.
    # return PrescriptionBase(
    #     image_path=img_path,
    #     ai_summary="",
    # )


@router.get("/{prescription_id}", response_model=Prescription)
def read_prescription(prescription_id: int, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found."
        )
    return prescription


@router.get("", response_model=List[Prescription])
def read_customer_prescriptions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        statement = select(Prescription).where(Prescription.customer_id == current_user.id)
        prescriptions = session.exec(statement).all()
    except Exception as e:
        prescriptions = []
        print(f"Error: {e}")

    return prescriptions
