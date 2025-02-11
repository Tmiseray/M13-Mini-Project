from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from circuitbreaker import circuit
from sqlalchemy import select


def fallback_function(customer):
    return None


# Save/Create New Customer Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data['name'] == 'Failure':
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(
                    name = customer_data['name'], 
                    email = customer_data['email'], 
                    phone = customer_data['phone']
                    )
                session.add(new_customer)
                session.commit()
            session.refresh(new_customer)
            return new_customer
        
    except Exception as e:
        raise e
    
# Read Customer Data
def read(id):
    query = select(Customer).where(id==id)
    customer = db.session.execute(query).scalar_one_or_none()
    if customer is None:
        raise Exception('No customer found with that ID')
    return customer

# Update Customer Data
def update(customer_data):
    query = select(Customer).where(id==customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    if customer is None:
        raise Exception('No customer found with that ID')
    
    customer.name = (customer_data['name'], customer.name)
    customer.email = (customer_data['email'], customer.email)
    customer.phone = (customer_data['phone'], customer.phone)
    db.session.commit()
    return customer

# Delete/Deactivate Customer
def deactivate(customer_data):
    query = select(Customer).where(id==customer_data['id'])
    customer = db.session.execute(query).scalar_one_or_none()
    if customer is None:
        raise Exception('No customer found with that ID')
    if customer.isActive == False:
        raise Exception('Customer is already deactivated')
    customer.deactivate()
    return customer

# Get All Customers
def find_all():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers