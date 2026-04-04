from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import CartItem, Order, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/carts", tags=["carts"])


@router.get("", response_model=List[CartItem])
def read_cart_items(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(CartItem).join(Order).where(Order.customer_id == current_user.id)
    cart_items = session.exec(statement).all()
    return cart_items


@router.get("/{cart_item_id}", response_model=CartItem)
def read_cart_item(
    cart_item_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    cart_item = session.get(CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    order = session.get(Order, cart_item.order_id)
    if order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return cart_item


@router.post("", response_model=CartItem)
def create_cart_item(
    *,
    session=Depends(get_session),
    cart_item_in: CartItem,
    current_user: User = Depends(get_current_user),
):
    order = session.get(Order, cart_item_in.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role != UserRole.CUSTOMER or order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.add(cart_item_in)
    session.commit()
    session.refresh(cart_item_in)
    return cart_item_in


@router.put("/{cart_item_id}", response_model=CartItem)
def update_cart_item(
    cart_item_id: int,
    *,
    session=Depends(get_session),
    cart_item_data: CartItem,
    current_user: User = Depends(get_current_user),
):
    db_cart_item = session.get(CartItem, cart_item_id)
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    order = session.get(Order, db_cart_item.order_id)
    if current_user.role != UserRole.CUSTOMER or order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    data_dict = cart_item_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_cart_item, key, value)

    session.add(db_cart_item)
    session.commit()
    session.refresh(db_cart_item)
    return db_cart_item


@router.delete("/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    cart_item = session.get(CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    order = session.get(Order, cart_item.order_id)
    if current_user.role != UserRole.CUSTOMER or order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(cart_item)
    session.commit()
    return {"ok": True}