from fastapi import FastAPI
from infrastructure.database import engine, Base
from api.routers import auth, users, products, orders, payments

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

api = FastAPI(
    title="Raízes do Nordeste API",
    description="Implementação Back-end(MVP) para uma rede de restaurantes.",
)

# Include all grouped resources
#api.include_router(auth.router)
#api.include_router(users.router)
#api.include_router(products.router)
#api.include_router(orders.router)
#api.include_router(payments.router)