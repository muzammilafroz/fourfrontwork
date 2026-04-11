from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..chatbot import ChatRequest, get_chatbot_response  # Renamed for clarity
from ..database import get_session
from ..models import User
from .user_routes import get_current_user

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("", response_model=dict)
async def chat_endpoint(
    request: ChatRequest,
    # session: Session = Depends(get_session), # Keep if you want to save history to DB
    current_user: User = Depends(get_current_user),
):
    """
    Handles the incoming chat request from the frontend.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated"
        )

    try:
        # CRITICAL: Added 'await' here
        response = await get_chatbot_response(request)
        return response

    except Exception as e:
        # This will be caught by FastAPI and returned as a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Service Error: {str(e)}",
        )
