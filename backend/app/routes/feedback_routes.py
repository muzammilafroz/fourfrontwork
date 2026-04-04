from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import Feedback, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("", response_model=List[Feedback])
def read_feedback(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.CUSTOMER:
        statement = select(Feedback).where(Feedback.customer_id == current_user.id)
    elif current_user.role in (UserRole.ADMIN, UserRole.EMPLOYEE):
        statement = select(Feedback)
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    feedbacks = session.exec(statement).all()
    return feedbacks


@router.get("/{feedback_id}", response_model=Feedback)
def read_feedback_item(
    feedback_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    feedback = session.get(Feedback, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if current_user.role == UserRole.CUSTOMER and feedback.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return feedback


@router.post("", response_model=Feedback)
def create_feedback(
    *,
    session=Depends(get_session),
    feedback_in: Feedback,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only customers can give feedback")

    feedback_in.customer_id = current_user.id

    session.add(feedback_in)
    session.commit()
    session.refresh(feedback_in)
    return feedback_in