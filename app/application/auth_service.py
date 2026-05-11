from app.infrastructure.repositories import AppRepository
from app.infrastructure.security import verify_password, create_access_token

class AuthService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def authenticate_user(self, email: str, password: str) -> dict:
        user = self.repo.get_user_by_email(email)
        
        # Validate existence and password match
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
            
        # Check if user is active
        if not user.is_active:
            raise PermissionError("User account is disabled")
        
        # Generate the token payload
        token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}