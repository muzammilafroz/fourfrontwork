from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from ..database import get_session
from ..models import MedicineRequest, User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/medicine-requests", tags=["medicine-requests"])


@router.get("", response_model=List[MedicineRequest])
def read_medicine_requests(
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.CUSTOMER:
        statement = select(MedicineRequest).where(
            MedicineRequest.requested_by == current_user.id
        )
    elif current_user.role in (UserRole.ADMIN, UserRole.EMPLOYEE):
        statement = select(MedicineRequest)
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

    requests = session.exec(statement).all()
    return requests


@router.get("/{request_id}", response_model=MedicineRequest)
def read_medicine_request(
    request_id: int,
    *,
    session=Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    request = session.get(MedicineRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Medicine request not found")

    if current_user.role == UserRole.CUSTOMER and request.requested_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return request


@router.post("", response_model=MedicineRequest)
def create_medicine_request(
    *,
    session=Depends(get_session),
    request_in: MedicineRequest,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(status_code=403, detail="Only customers can request medicines")

    request_in.requested_by = current_user.id

    session.add(request_in)
    session.commit()
    session.refresh(request_in)
    return request_in


@router.put("/{request_id}", response_model=MedicineRequest)
def update_medicine_request(
    request_id: int,
    *,
    session=Depends(get_session),
    request_data: MedicineRequest,
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in (UserRole.ADMIN, UserRole.EMPLOYEE):
        raise HTTPException(status_code=403, detail="Only employees can update requests")

    db_request = session.get(MedicineRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Medicine request not found")

    data_dict = request_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(db_request, key, value)

    db_request.handled_by = current_user.id

    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request