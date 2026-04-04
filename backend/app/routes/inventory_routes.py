from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import Medicine, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=List[Medicine])
def read_inventory(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Medicine)
    medicines = session.exec(statement).all()
    return medicines


@router.get("/{medicine_id}", response_model=Medicine)
def read_medicine(
    medicine_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.post("", response_model=Medicine)
def create_medicine(
    *,
    session=Depends(get_session),
    medicine_in: Medicine,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create medicine")

    session.add(medicine_in)
    session.commit()
    session.refresh(medicine_in)
    return medicine_in


@router.put("/{medicine_id}", response_model=Medicine)
def update_medicine(
    medicine_id: int,
    *,
    session=Depends(get_session),
    medicine_data: Medicine,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update medicine")

    db_medicine = session.get(Medicine, medicine_id)
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    data_dict = medicine_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_medicine, key, value)

    session.add(db_medicine)
    session.commit()
    session.refresh(db_medicine)
    return db_medicine


@router.delete("/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete medicine")

    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    session.delete(medicine)
    session.commit()
    return {"ok": True}