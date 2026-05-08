import random
from app.infrastructure.repositories import AppRepository
from app.domain.enums import OrderStatusEnum
from app.api.schemas import PaymentMockRequest

class PaymentService:
    def __init__(self, repository: AppRepository):
        self.repository = repository

    def process_mock_payment(self, req: PaymentMockRequest, user_id: int) -> dict:
        order = self.repository.get_order_by_id(req.order_id)
        
        if not order:
            raise ValueError("Order not found!")
        
        if order.status != OrderStatusEnum.CREATED:
            raise ValueError("The order has already been processed")

        # Random External Payment Failure 
        is_gateway_approved = random.random() <= 0.80 

        if not is_gateway_approved:
            order.status = OrderStatusEnum.CANCELED
            self.repository.update_order(order)
            
            self.repository.create_audit_log(
                user_id=user_id,
                action="CANCELED",
                resource_id=f"Order_{order.id}",
                details="External payment gateway failure"
            )
            
            return {
                "message": "Payment declined by the card operator",
                "new_status": order.status
            }

        # Approved Payment
        order.status = OrderStatusEnum.PAID 
        self.repository.update_order(order)
        
        self.repository.create_audit_log(
            user_id=user_id,
            action="PAID",
            resource_id=f"Order_{order.id}",
            details=f"Payment approved by gateway"
        )
        
        return {
            "message": "Payment approved successfully",
            "new_status": order.status
        }