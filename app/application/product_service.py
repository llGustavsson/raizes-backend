from infrastructure.repositories import AppRepository
from infrastructure.orm_models import Product

class ProductService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def get_active_menu(self) -> list[Product]:
        # Currently just a pass-through to the repository, but ready for future business rules
        return self.repo.get_available_products()