from app.infrastructure.database import Base, SessionLocal, engine
from app.infrastructure.orm_models import Product

# Ensure tables are created
Base.metadata.create_all(bind=engine)

# Initial menu data
INITIAL_PRODUCTS = [
    {"name": "Prato 1", "price": 25.90, "is_available": True},
    {"name": "Prato 2", "price": 35.50, "is_available": True},
    {"name": "Prato 3", "price": 28.00, "is_available": True},
    {"name": "Acompanhamento 1", "price": 12.00, "is_available": True},
    {"name": "Acompanhamento 2", "price": 16.00, "is_available": True},
    {"name": "Suco 1", "price": 6.50, "is_available": True},
    {"name": "Suco 2", "price": 9.00, "is_available": True},
    {"name": "Suco 3", "price": 18.00, "is_available": True},
    {"name": "Suco 4", "price": 15.00, "is_available": False}, # Example of unavailable item
]

def seed_database():
    db = SessionLocal()
    try:
        print("Checking products in the database...")
        # Check if the table already has data
        existing_products_count = db.query(Product).count()
        
        if existing_products_count > 0:
            print(f"Database already has {existing_products_count} products. Skipping seed.")
            return

        print("Populating the database with initial menu...")
        for item_data in INITIAL_PRODUCTS:
            product = Product(
                name=item_data["name"],
                price=item_data["price"],
                is_available=item_data["is_available"]
            )
            db.add(product)
            
        db.commit()
        print("Database successfully seeded!")
        
    except Exception as e:
        db.rollback()
        print(f"Error while seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()