from fastapi import APIRouter, Depends
from typing import List
from app.application.product_service import ProductService
from app.api.schemas import ProductResponse
from app.api.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["Products (Menu)"])

@router.get("", response_model=List[ProductResponse])
def get_menu(service: ProductService = Depends(get_product_service)):
    return service.get_active_menu()