from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from ..auth import oauth2_scheme
from ..config import settings
from ..crud import get_user_by_email
from ..database import get_session
from ..models import Message, User, UserPublic, UserRole, UserStatus

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
    suspended_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Your account has been suspended.",
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

    if user.status == UserStatus.SUSPENDED:
        raise suspended_exception

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


@router.get(
    "/all",
    response_model=list[UserPublic],
    summary="List all users",
    description="Retrieves a list of all users in the system. This endpoint is typically restricted to admin users.",
    responses={
        200: {
            "model": list[UserPublic],
            "description": "A list of user profiles.",
        },
        401: {
            "model": Message,
            "description": "Unauthorized - Token is invalid or expired.",
        },
    },
)
def read_all_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieves all users from the database. Access may be restricted based on user roles.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to view all users")

    # select all except admin
    # users = session.exec(select(User).where(User.role != UserRole.ADMIN)).all()
    users = session.exec(select(User)).all()
    return users


# Update a user's status to suspended or active.
@router.put(
    "/{user_id}/status",
    response_model=Message,
    summary="Block a user",
    description="Blocks a user by setting their status to 'blocked'. Only admin users can perform this action.",
    responses={
        200: {
            "model": Message,
            "description": "User blocked successfully.",
        },
        401: {
            "model": Message,
            "description": "Unauthorized - Token is invalid or expired.",
        },
    },
)
def toggle_status(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Blocks a user by updating their status in the database. Only accessible to admin users.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized to block users")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Cannot block an admin user")

    if user.status == UserStatus.ACTIVE:
        user.status = UserStatus.SUSPENDED
    else:
        user.status = UserStatus.ACTIVE

    session.add(user)
    session.commit()
    return {"detail": f"User with ID {user_id}'s status has been updated."}
