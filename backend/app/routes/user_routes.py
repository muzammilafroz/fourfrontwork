from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session

from ..auth import oauth2_scheme
from ..config import settings
from ..crud import get_user_by_email
from ..database import get_session
from ..models import Message, User, UserPublic

router = APIRouter(prefix="/user", tags=["Users"])


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    """
    Decodes the JWT token and validates the user exists in the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: None | str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(session, email=email)

    if user is None:
        raise credentials_exception

    return user


@router.get(
    "/logout",
    response_model=Message,
    summary="Log out current user",
    description="Logs the user out by invalidating the current session. Note: Since JWT is stateless, the client should also delete the token locally.",
    responses={
        200: {
            "description": "Successful logout message.",
            "content": {
                "application/json": {"example": {"detail": "Successfully logged out."}}
            },
        },
        401: {"description": "Unauthorized - Invalid or missing token."},
    },
)
def logout(_: UserPublic = Depends(get_current_user)):
    return {"detail": "Successfully logged out."}


@router.get(
    "/me",
    # This ensures the API documentation reflects the public schema, not the internal DB model
    response_model=UserPublic,
    summary="Get current user profile",
    description="Retrieves the full profile details of the currently authenticated user based on the provided Bearer token.",
    response_description="The public user profile data.",
    responses={
        200: {
            "model": UserPublic,
            "description": "User profile retrieved successfully.",
        },
        401: {
            "model": Message,
            "description": "Unauthorized - Token is invalid or expired.",
        },
    },
)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Returns the user object retrieved by the 'get_current_user' dependency.
    """
    return current_user
