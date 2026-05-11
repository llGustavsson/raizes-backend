from app.infrastructure.repositories import AppRepository
from app.infrastructure.orm_models import Product

class ProductService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def get_active_menu(self) -> list[Product]:
        return self.repo.get_available_products()