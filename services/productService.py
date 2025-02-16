from sqlalchemy.orm import Session
from database import db
from models.product import Product
from circuitbreaker import circuit
from sqlalchemy import select


def fallback_function(product):
    return None


# Save/Create New Product Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(product_data):
    try:
        if product_data['name'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_product = Product(
                    name = product_data['name'], 
                    price = product_data['price'], 
                    createdBy = product_data['createdBy']
                    )
                session.add(new_product)
                session.commit()
            session.refresh(new_product)
            return new_product
        
    except Exception as e:
        raise e
    
# Read Product Data
def read(id):
    query = select(Product).where(Product.id==id)
    product = db.session.execute(query).scalar_one_or_none()
    if product is None:
        raise Exception('No product found with that ID')
    return product

# Update Product Data
def update(product_data):
    query = select(Product).where(Product.id==product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    if product is None:
        raise Exception('No product found with that ID')
    
    product.name = product_data.get('name', product.name)
    product.price = product_data.get('price', product.price)
    product.updatedBy = product_data.get('updatedBy', product.updatedBy)
    db.session.commit()
    return product

# Delete/Deactivate Product
def deactivate(product_data):
    query = select(Product).where(Product.id==product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    if product is None:
        raise Exception('No product found with that ID')
    if not product.isActive:
        raise Exception('Product is already deactivated')
    product.deactivate()
    return product

# Activate Product
def activate(product_data):
    query = select(Product).where(Product.id==product_data['id'])
    product = db.session.execute(query).scalar_one_or_none()
    if product is None:
        raise Exception('No product found with that ID')
    if product.isActive:
        raise Exception('Product is already activated')
    product.activate()
    return product

# Get All Products
def find_all():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products