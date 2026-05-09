from app.infrastructure.repositories import AppRepository
from app.infrastructure.orm_models import User
from app.infrastructure.security import hash_password
from app.api.schemas import UserCreate, UserUpdate

class UserService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def create_user(self, user_in: UserCreate) -> User:
        if not user_in.lgpd_consent:
            raise ValueError("LGPD consent is required")
            
        if self.repo.get_user_by_email(user_in.email):
            raise ValueError("Email already registered")
            
        new_user = User(
            full_name=user_in.full_name,
            email=user_in.email,
            password_hash=hash_password(user_in.password),
            lgpd_consent=user_in.lgpd_consent
        )
        return self.repo.save_user(new_user)

    def update_profile(self, current_user: User, update_data: UserUpdate) -> User:
        if update_data.full_name:
            current_user.full_name = update_data.full_name
        if update_data.password:
            current_user.password_hash = hash_password(update_data.password)
            
        return self.repo.save_user(current_user)