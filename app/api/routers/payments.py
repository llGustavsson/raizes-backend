from fastapi import APIRouter, Depends, HTTPException
from app.application.payment_service import PaymentService
from app.infrastructure.orm_models import User
from app.api.schemas import PaymentMockRequest
from app.api.dependencies import get_payment_service, get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/mock")
def confirm_payment(
    req: PaymentMockRequest, 
    service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(get_current_user)
):
    try:
        order = service.process_mock_payment(current_user.id, req.order_id, req.amount_paid)
        return {
            "message": "Payment successful. Order sent to kitchen.",
            "transaction_id": "tx_mocked_12345",
            "new_status": order.status
        }
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))