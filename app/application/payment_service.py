from app.infrastructure.repositories import AppRepository
from app.domain.enums import OrderStatusEnum

class PaymentService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def process_mock_payment(self, user_id: int, order_id: int, amount_paid: float):
        order = self.repo.get_order_by_id(order_id)
        
        if not order:
            raise ValueError("Order not found")
        if order.user_id != user_id:
            raise PermissionError("Not authorized to pay for this order")
        if order.status != OrderStatusEnum.CREATED:
            raise ValueError("Order is already paid or canceled")
        if amount_paid < order.total:
            raise ValueError(f"Insufficient amount. Total is ${order.total}")

        # Process successful payment
        order.status = OrderStatusEnum.PAID
        self.repo.update_order(order)
        
        return order