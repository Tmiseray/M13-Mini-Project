from sqlalchemy.orm import Session
from database import db
from models.order import Order
from models.product import Product
from circuitbreaker import circuit
from sqlalchemy import select


def fallback_function(order):
    return None


# Save/Create New Order Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(order_data):
    try:
        if order_data['customerId'] == 'Failure':
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                product = session.get(Product, order_data['productId'])
                if not product:
                    raise ValueError('Invalid product ID')
                
                totalPrice = round((order_data['quantity'] * product.price), 2)
                new_order = Order(
                    customerId = order_data['customerId'],
                    productId = order_data['productId'],
                    quantity = order_data['quantity'],
                    totalPrice = totalPrice
                )
                session.add(new_order)
                session.commit()
            session.refresh(new_order)
            return new_order
        
    except Exception as e:
        raise e
    
# Read Order Data
def read(id):
    query = select(Order).where(Order.id==id)
    order = db.session.execute(query).scalar_one_or_none()
    if order is None:
        raise Exception('No order found with that ID')
    return order

# Update Order Data
def update(order_data):
    query = select(Order).where(Order.id==order_data['id'])
    order = db.session.execute(query).scalar_one_or_none()
    if order is None:
        raise Exception('No order found with that ID')
    
    order.customerId = order.customerId
    order.productId = order_data.get('productId', order.productId)
    order.quantity = order_data.get('quantity', order.quantity)
    db.session.commit()
    return order

# Delete Order
def delete(order_data):
    query = select(Order).where(Order.id==order_data['id'])
    order = db.session.execute(query).scalar_one_or_none()
    if order is None:
        raise Exception('No order found with that ID')
    db.session.delete(order)
    db.session.commit()

# Get All Orders
def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders