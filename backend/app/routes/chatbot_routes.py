from fastapi import APIRouter, Depends, HTTPException, status

from ..chat import get_customer_chatbot_response
from ..chatbot import ChatRequest, get_chatbot_response
from ..models import User, UserRole
from .user_routes import get_current_user

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("", response_model=dict)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Handles the incoming chat request from the frontend.
    Routes to the appropriate chatbot based on user role.
    """
    handler = (
        get_customer_chatbot_response
        if current_user.role == UserRole.CUSTOMER
        else get_chatbot_response
    )

    try:
        return await handler(request)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI Service Error",
        )
