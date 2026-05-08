from fastapi import FastAPI
from app.infrastructure.database import engine, Base, get_db
from app.api.routers import auth, users, products, orders, payments
from app.domain.exception_handler import register_exception_handlers

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
get_db()

api = FastAPI(
    title="Raízes do Nordeste API",
    description="Implementação Back-end(MVP) para uma rede de restaurantes.",
)

# Exception Handler
register_exception_handlers(api)

# Include all grouped resources
api.include_router(auth.router)
api.include_router(users.router)
api.include_router(products.router)
api.include_router(orders.router)
api.include_router(payments.router)