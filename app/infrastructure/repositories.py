from sqlalchemy.orm import Session
from app.infrastructure.orm_models import User, Product, Order, OrderItem

class AppRepository:
    def __init__(self, db: Session):
        self.db = db

    # User Methods
    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()
        
    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def save_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # Product Methods
    def get_available_products(self):
        return self.db.query(Product).filter(Product.is_available == True).all()
        
    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    # Order Methods
    def create_order(self, order: Order, items: list[OrderItem]):
        self.db.add(order)
        self.db.flush() # Get order ID without committing yet
        for item in items:
            item.order_id = order.id
            self.db.add(item)
        self.db.commit()
        self.db.refresh(order)
        return order
        
    def get_order_by_id(self, order_id: int) -> Order:
        return self.db.query(Order).filter(Order.id == order_id).first()
        
    def update_order(self, order: Order):
        self.db.commit()
        self.db.refresh(order)
        return order