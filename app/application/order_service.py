from infrastructure.repositories import AppRepository
from infrastructure.orm_models import Order, OrderItem
from domain.enums import OrderStatusEnum
from api.schemas import OrderCreate

class OrderService:
    def __init__(self, repo: AppRepository):
        self.repo = repo

    def create_order(self, user_id: int, order_in: OrderCreate) -> Order:
        order = Order(user_id=user_id, channel=order_in.channel, status=OrderStatusEnum.CREATED)
        items = []
        total = 0.0
        
        # Business Logic: Validate availability and calculate total securely
        for item_in in order_in.items:
            product = self.repo.get_product_by_id(item_in.product_id)
            if not product:
                raise ValueError(f"Product ID {item_in.product_id} not found.")
            if not product.is_available:
                raise ValueError(f"Product '{product.name}' is currently unavailable.")
                
            items.append(OrderItem(product_id=product.id, quantity=item_in.quantity, unit_price=product.price))
            total += (product.price * item_in.quantity)
            
        order.total = total
        return self.repo.create_order(order, items)