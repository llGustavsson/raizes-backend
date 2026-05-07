import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from infrastructure.security import decode_token
from infrastructure.repositories import AppRepository

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