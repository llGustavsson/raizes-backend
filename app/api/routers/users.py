from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.orm_models import User
from api.schemas import UserCreate, UserUpdate, UserResponse
from application.user_service import UserService
from api.dependencies import get_current_user, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user_in)
    except ValueError as e:
        # Translates business error to HTTP error
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/me", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate, 
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    return service.update_profile(current_user, update_data)