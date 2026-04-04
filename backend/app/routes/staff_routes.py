from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/staff", tags=["staff"])


@router.get("", response_model=List[User])
def read_staff(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can view staff")

    statement = select(User).where(User.role == UserRole.EMPLOYEE)
    staff = session.exec(statement).all()
    return staff


@router.get("/{staff_id}", response_model=User)
def read_staff_member(
    staff_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can view staff")

    staff = session.get(User, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    if staff.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=404, detail="Staff member not found")

    return staff


@router.post("", response_model=User)
def create_staff(
    *,
    session=Depends(get_session),
    staff_in: User,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create staff")

    staff_in.role = UserRole.EMPLOYEE

    session.add(staff_in)
    session.commit()
    session.refresh(staff_in)
    return staff_in


@router.put("/{staff_id}", response_model=User)
def update_staff(
    staff_id: int,
    *,
    session=Depends(get_session),
    staff_data: User,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update staff")

    db_staff = session.get(User, staff_id)
    if not db_staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    data_dict = staff_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_staff, key, value)

    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete staff")

    staff = session.get(User, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    if staff.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=404, detail="Staff member not found")

    session.delete(staff)
    session.commit()
    return {"ok": True}