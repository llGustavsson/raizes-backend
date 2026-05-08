from fastapi import APIRouter, Depends, HTTPException, status
from application.order_service import OrderService
from infrastructure.orm_models import User
from api.schemas import OrderCreate, OrderResponse
from api.dependencies import get_order_service, get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate, 
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return service.create_order(current_user.id, order_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))