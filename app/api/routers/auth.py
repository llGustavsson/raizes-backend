from fastapi import APIRouter, Depends, HTTPException, status
from application.auth_service import AuthService
from api.schemas import LoginRequest, TokenResponse
from api.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        # The router just passes the data to the service
        return service.authenticate_user(req.email, req.password)
    except ValueError as e:
        # Translates wrong credentials to HTTP 401 Unauthorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except PermissionError as e:
        # Translates disabled account to HTTP 403 Forbidden
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

