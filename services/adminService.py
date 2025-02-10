from sqlalchemy.orm import Session
from database import db
from models.admin import Admin
from circuitbreaker import circuit
from sqlalchemy import select


def fallback_function(admin):
    return None


# Save/Create New admin Data
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(admin_data):
    try:
        if admin_data['name'] == 'Failure':
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_admin = Admin(name=admin_data['name'], email=admin_data['email'], phone=admin_data['phone'])
                session.add(new_admin)
                session.commit()
            session.refresh(new_admin)
            return new_admin
        
    except Exception as e:
        raise e
    
# Read admin Data
def read(id):
    query = select(Admin).where(id==id)
    admin = db.session.execute(query).scalar_one_or_none()
    if admin == None:
        raise Exception('No admin found with that ID')
    return admin

# Update admin Data
def update(admin_data):
    query = select(Admin).where(id==admin_data['id'])
    admin = db.session.execute(query).scalar_one_or_none()
    if admin == None:
        raise Exception('No admin found with that ID')
    
    admin.name = (admin_data['name'], admin.name)
    admin.email = (admin_data['email'], admin.email)
    admin.phone = (admin_data['phone'], admin.phone)
    db.session.commit()
    return admin

# Delete/Deactivate admin
def deactivate(admin_data):
    query = select(Admin).where(id==admin_data['id'])
    admin = db.session.execute(query).scalar_one_or_none()
    if admin == None:
        raise Exception('No admin found with that ID')
    if admin.isActive == False:
        raise Exception('Admin is already deactivated')
    admin.deactivate()
    return admin

# Get All admins
def find_all():
    query = select(Admin)
    admins = db.session.execute(query).scalars().all()
    return admins