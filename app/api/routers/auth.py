from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.application.auth_service import AuthService
from app.api.schemas import UserResponse, TokenResponse
from app.api.dependencies import get_auth_service, get_current_user
from app.infrastructure.orm_models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service: AuthService = Depends(get_auth_service)
):
    try:
        # The Swagger UI form natively sends the email inside the 'username' field.
        # We pass form_data.username as the email to our service.
        return service.authenticate_user(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.get("/verify", response_model=UserResponse)
def verify_token(current_user: User = Depends(get_current_user)):
    
    return current_user