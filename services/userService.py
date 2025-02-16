from sqlalchemy.orm import Session
from database import db
from models.user import User
from circuitbreaker import circuit
from sqlalchemy import select


def fallback_function(user):
    return None


# Save/Create New User Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(user_data):
    try:
        if user_data['name'] == 'Failure':
            raise Exception('Failure condition triggered')
        
        if user_data['role'] == '@Dm!n1$+rAT0R':
            user_role = 'admin'
        else:
            user_role = 'user'
        
        with Session(db.engine) as session:
            with session.begin():
                new_user = User(
                    name = user_data['name'], 
                    email = user_data['email'], 
                    phone = user_data['phone'],
                    role = user_role
                    )
                session.add(new_user)
                session.commit()
            session.refresh(new_user)
            return new_user
        
    except Exception as e:
        raise e
    
# Read User Data
def read(id):
    query = select(User).where(User.id==id)
    user = db.session.execute(query).scalar_one_or_none()
    if user is None:
        raise Exception('No user found with that ID')
    return user

# Update User Data
def update(user_data):
    query = select(User).where(User.id==user_data['id'])
    user = db.session.execute(query).scalar_one_or_none()
    if user is None:
        raise Exception('No user found with that ID')
    
    if user_data['role'] == '@Dm!n1$+rAT0R':
        user_role = 'admin'
    else:
        user_role = 'user'
    
    user.name = user_data.get('name', user.name)
    user.email = user_data.get('email', user.email)
    user.phone = user_data.get('phone', user.phone)
    user.role = user_role
    db.session.commit()
    return user

# Delete/Deactivate User
def deactivate(user_data):
    query = select(User).where(User.id==user_data['id'])
    user = db.session.execute(query).scalar_one_or_none()
    if user is None:
        raise Exception('No user found with that ID')
    if not user.isActive:
        raise Exception('User is already deactivated')
    user.deactivate()
    return user

# Activate User
def activate(user_data):
    query = select(User).where(User.id==user_data['id'])
    user = db.session.execute(query).scalar_one_or_none()
    if user is None:
        raise Exception('No user found with that ID')
    if user.isActive:
        raise Exception('User is already activated')
    user.activate()
    return user

# Get All Users/Admins/Customers
def find_all():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users

def find_all_admins():
    query = select(User).where(User.role=='admin')
    admins = db.session.execute(query).scalars().all()
    return admins

def find_all_customers():
    query = select(User).where(User.role=='user')
    customers = db.session.execute(query).scalars().all()
    return customers