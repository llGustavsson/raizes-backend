from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.repositories import AppRepository
from infrastructure.orm_models import User
from infrastructure.security import hash_password
from api.schemas import UserCreate, UserUpdate, UserResponse
from api.dependencies import get_repository, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, repo: AppRepository = Depends(get_repository)):
    if not user_in.lgpd_consent:
        raise HTTPException(status_code=400, detail="LGPD consent is required")
        
    if repo.get_user_by_email(user_in.email):
        raise HTTPException(status_code=409, detail="Email already registered")
        
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        lgpd_consent=user_in.lgpd_consent
    )
    return repo.save_user(new_user)

@router.patch("/me", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate, 
    repo: AppRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user)
):
    if update_data.name:
        current_user.name = update_data.name
    if update_data.password:
        current_user.password_hash = hash_password(update_data.password)
        
    return repo.save_user(current_user)