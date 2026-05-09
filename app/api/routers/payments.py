from fastapi import APIRouter, Depends, HTTPException
from app.application.payment_service import PaymentService
from app.infrastructure.orm_models import User
from app.infrastructure.repositories import AppRepository
from app.api.schemas import PaymentMockRequest
from app.api.dependencies import get_current_user, get_repository

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/mock")
def confirm_payment(
    req: PaymentMockRequest, 
    rep: AppRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user)
):
    
    service = PaymentService(rep)
    
    try:
        return service.process_mock_payment(req=req, user_id=current_user.id)
        
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))