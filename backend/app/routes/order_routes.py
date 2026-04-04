from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import Order, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[Order])
def read_orders(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.CUSTOMER:
        statement = select(Order).where(Order.customer_id == current_user.id)
    elif current_user.role in (UserRole.ADMIN, UserRole.EMPLOYEE):
        statement = select(Order)
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    orders = session.exec(statement).all()
    return orders


@router.get("/{order_id}", response_model=Order)
def read_order(
    order_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role == UserRole.CUSTOMER and order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return order


@router.post("", response_model=Order)
def create_order(
    *,
    session=Depends(get_session),
    order_in: Order,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only customers can create orders")

    order_in.customer_id = current_user.id
    order_in.customer_name = current_user.name
    order_in.customer_phone = current_user.phone

    session.add(order_in)
    session.commit()
    session.refresh(order_in)
    return order_in


@router.put("/{order_id}", response_model=Order)
def update_order(
    order_id: int,
    *,
    session=Depends(get_session),
    order_data: Order,
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in (UserRole.ADMIN, UserRole.EMPLOYEE):
        raise HTTPException(status_code=403, detail="Only employees can update orders")

    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    data_dict = order_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_order, key, value)

    if current_user.role == UserRole.EMPLOYEE:
        db_order.employee_id = current_user.id

    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order