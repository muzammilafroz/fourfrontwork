from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.crud import image_to_base64, save_base64_image
from app.llm import extract_prescription_data

from ..database import get_session
from ..models import (
    Medication,
    Message,
    Prescription,
    PrescriptionCreate,
    PrescriptionPublic,
    User,
)
from .user_routes import get_current_user

router = APIRouter(prefix="/prescriptions", tags=["prescription"])


@router.post(
    "/create",
    response_model=PrescriptionPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create and process a new prescription",
    description="""
    Uploads a base64 encoded image of a prescription.

    1. Saves the image to the server.
    2. Uses AI to extract medication names, dosages, and doctor information.
    3. Saves the extracted data to the database linked to the current user.

    """,
    responses={
        201: {"description": "Prescription successfully processed and saved."},
        401: {"model": Message, "description": "Unauthorized - Valid token required."},
        500: {
            "model": Message,
            "description": "Internal Server Error - AI extraction or database save failed.",
        },
    },
)
def create_prescription(
    prescription_in: PrescriptionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a prescription image, extract data using AI, and save to database. The user must be authenticated to perform this action.
    """

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


@router.get(
    "/{prescription_id}",
    response_model=PrescriptionPublic,
    summary="Get prescription by ID",
    description="Retrieves the details of a specific prescription. The user must be the admin of the prescription.",
    responses={
        200: {"description": "Prescription details retrieved successfully."},
        403: {
            "model": Message,
            "description": "Forbidden - You do not own this prescription.",
        },
        404: {"model": Message, "description": "Prescription not found."},
    },
)
def read_prescription(
    prescription_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific prescription by ID.
    """
    prescription = session.get(Prescription, prescription_id)

    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found."
        )

    if prescription.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Prescription is not yours."
        )
    return prescription


@router.get(
    "",
    response_model=List[PrescriptionPublic],
    summary="List all my prescriptions",
    description="Retrieves a list of all prescriptions belonging to the authenticated user.",
    response_description="A list containing the user's prescription history.",
)
def read_customer_prescriptions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get all prescriptions for the current user.
    """

    try:
        statement = select(Prescription).where(
            Prescription.customer_id == current_user.id
        )
        prescriptions = session.exec(statement).all()
    except Exception as e:
        prescriptions = []
        print(f"Error: {e}")

    for prescription in prescriptions:
        prescription.image_base64 = image_to_base64(prescription.image_path)

    return prescriptions
