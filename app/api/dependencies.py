import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.security import decode_token
from infrastructure.repositories import AppRepository
from application.user_service import UserService
from application.order_service import OrderService
from application.payment_service import PaymentService
from application.auth_service import AuthService
from application.product_service import ProductService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_repository(db: Session = Depends(get_db)):
    return AppRepository(db)

def get_current_user(token: str = Depends(oauth2_scheme), repo: AppRepository = Depends(get_repository)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        user = repo.get_user_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
            
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_user_service(repo: AppRepository = Depends(get_repository)) -> UserService:
    return UserService(repo)

def get_auth_service(repo: AppRepository = Depends(get_repository)) -> AuthService:
    return AuthService(repo)

def get_product_service(repo: AppRepository = Depends(get_repository)) -> ProductService:
    return ProductService(repo)

def get_order_service(repo: AppRepository = Depends(get_repository)) -> OrderService:
    return OrderService(repo)

def get_payment_service(repo: AppRepository = Depends(get_repository)) -> PaymentService:
    return PaymentService(repo)
