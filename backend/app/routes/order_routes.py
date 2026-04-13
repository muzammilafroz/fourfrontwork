from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from ..database import get_session
from ..models import CartItem, Medicine, Order, OrderCreate, OrderPublic, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=List[OrderPublic])
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


@router.get("/{order_id}", response_model=OrderPublic)
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


@router.post("", response_model=OrderPublic)
def create_order(
    *,
    session=Depends(get_session),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in (UserRole.ADMIN, UserRole.EMPLOYEE):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employees can create orders",
        )

    if current_user.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required"
        )

    # Because the Order model requires customer_id, we look up the user by phone.
    customer = session.exec(
        select(User).where(User.phone == order_in.customer_phone)
    ).first()

    if not customer:
        customer = session.exec(select(User).where(User.id == 1)).first()

    # We exclude 'cart_items' from the dump because Order (table) doesn't have that column
    order_data = order_in.model_dump(exclude={"cart_items"})
    db_order = Order(**order_data, customer_id=customer.id, employee_id=current_user.id)

    session.add(db_order)
    session.flush()  # Populates db_order.id for the cart items to use

    # 4. Create the Cart Items
    for item_in in order_in.cart_items:
        # Verify medicine exists
        medicine = session.get(Medicine, item_in.medicine_id)
        if not medicine:
            raise HTTPException(
                status_code=404, detail=f"Medicine ID {item_in.medicine_id} not found"
            )

        if medicine.stock_quantity < item_in.quantity:
            raise HTTPException(
                status_code=400, detail=f"Not enough stock for {medicine.name}"
            )
        medicine.stock_quantity -= item_in.quantity

        db_cart_item = CartItem(**item_in.model_dump(), order_id=db_order.id)
        session.add(db_cart_item)

    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=500, detail="Database error during order creation"
        )

    session.refresh(db_order)
    return db_order


@router.put("/{order_id}", response_model=OrderPublic)
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
