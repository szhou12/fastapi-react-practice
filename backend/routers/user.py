from fastapi import APIRouter, Depends

from ..auth.auth_handler import get_current_active_user
from ..schemas import UserResponse
from ..models import User

router = APIRouter()

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Notice that the dependency get_current_active_user returns a SQLAlchemy ORM object (User)
    but this endpoint returns a Pydantic model object (UserResponse)
    FastAPI seems to automatically handle model conversion and translate database model supported by SQLAlchemy.
    """
    return current_user

