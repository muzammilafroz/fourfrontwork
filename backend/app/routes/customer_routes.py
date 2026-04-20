from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=List[User])
def read_customers(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in (UserRole.ADMIN, UserRole.EMPLOYEE):
        raise HTTPException(status_code=403, detail="Not authorized to view customers")

    statement = select(User).where(User.role == UserRole.CUSTOMER)
    customers = session.exec(statement).all()
    return customers


@router.get("/{customer_id}", response_model=User)
def read_customer(
    customer_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    customer = session.get(User, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if (
        current_user.role not in (UserRole.ADMIN, UserRole.EMPLOYEE)
        and current_user.id != customer_id
    ):
        raise HTTPException(status_code=403, detail="Not authorized")

    if customer.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.put("/{customer_id}", response_model=User)
def update_customer(
    customer_id: int,
    *,
    session=Depends(get_session),
    customer_data: User,
    current_user: User = Depends(get_current_user),
):
    if current_user.id != customer_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_customer = session.get(User, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if db_customer.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=404, detail="Customer not found")

    data_dict = customer_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_customer, key, value)

    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer
