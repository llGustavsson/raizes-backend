from fastapi import APIRouter, Depends, HTTPException
from infrastructure.security import verify_password, create_access_token
from infrastructure.repositories import AppRepository
from api.schemas import LoginRequest, TokenResponse
from api.dependencies import get_repository

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, repo: AppRepository = Depends(get_repository)):
    user = repo.get_user_by_email(req.email)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
