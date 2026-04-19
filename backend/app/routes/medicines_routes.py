from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, col, or_, select

from ..database import get_session
from ..models import (
    Medicine,
    MedicineCreate,
    MedicinePublic,
    User,
    UserRole,
)
from .user_routes import get_current_user

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post(
    "",
    response_model=MedicinePublic,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new medicine",
    description="Adds a new medicine to the inventory. Typically restricted to Admin users.",
)
def create_medicine(
    *,
    session: Session = Depends(get_session),
    medicine_in: MedicineCreate,
    current_user: User = Depends(get_current_user),
):
    db_medicine = Medicine.model_validate(medicine_in)

    if current_user.role == UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only staff can add medicines")

    session.add(db_medicine)
    session.commit()
    session.refresh(db_medicine)

    return db_medicine


@router.get(
    "",
    response_model=List[MedicinePublic],
    summary="List all medicines",
    description="Retrieve a list of available medicines with optional pagination.",
)
def read_medicines(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    search: Optional[str] = None,
):
    statement = select(Medicine).offset(offset).limit(limit)

    if search:
        statement = statement.where(
            or_(
                col(Medicine.name).icontains(search),
                col(Medicine.composition).icontains(search),
                col(Medicine.brand).icontains(search),
            )
        )

    medicines = session.exec(statement).all()
    return medicines


@router.delete(
    "/{medicine_id}",
    summary="Delete a medicine",
    description="Deletes a medicine from the inventory. Typically restricted to Admin users.",
)
def delete_medicine(
    medicine_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only staff can delete medicines")

    medicine = session.get(Medicine, medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    session.delete(medicine)
    session.commit()
    return {"ok": True}


# @router.get(
#     "/{medicine_id}", response_model=MedicinePublic, summary="Get medicine by ID"
# )
# def read_medicine(medicine_id: int, session: Session = Depends(get_session)):
#     medicine = session.get(Medicine, medicine_id)
#     if not medicine:
#         raise HTTPException(status_code=404, detail="Medicine not found")
#     return medicine


@router.put(
    "/{medicine_id}", response_model=MedicinePublic, summary="Update medicine details"
)
def update_medicine(
    *,
    session: Session = Depends(get_session),
    medicine_id: int,
    medicine_in: MedicineCreate,
):
    db_medicine = session.get(Medicine, medicine_id)
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # Convert input data to dict, excluding fields not set by the user
    medicine_data = medicine_in.model_dump(exclude_unset=True)
    for key, value in medicine_data.items():
        setattr(db_medicine, key, value)

    session.add(db_medicine)
    session.commit()
    session.refresh(db_medicine)
    return db_medicine


# @router.delete("/{medicine_id}", summary="Delete a medicine")
# def delete_medicine(medicine_id: int, session: Session = Depends(get_session)):
#     medicine = session.get(Medicine, medicine_id)
#     if not medicine:
#         raise HTTPException(status_code=404, detail="Medicine not found")

#     session.delete(medicine)
#     session.commit()
#     return {"ok": True}
