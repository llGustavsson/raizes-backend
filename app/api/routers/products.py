from fastapi import APIRouter, Depends
from typing import List
from application.product_service import ProductService
from api.schemas import ProductResponse
from api.dependencies import get_product_service

router = APIRouter(prefix="/products", tags=["Products (Menu)"])

@router.get("", response_model=List[ProductResponse])
def get_menu(service: ProductService = Depends(get_product_service)):
    return service.get_active_menu()