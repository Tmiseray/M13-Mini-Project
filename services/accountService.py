from sqlalchemy.orm import Session
from database import db
from models.account import Account
from circuitbreaker import circuit
from sqlalchemy import select
from utils.util import encode_token
import bcrypt


def fallback_function(account):
    return None


# Account Login
def login(username, password):
    query = select(Account).where(Account.username == username)
    user = db.session.execute(query).scalar_one_or_none()

    if user and bcrypt.checkpw(
        password.encode('utf-8'),
        user.password
    ):
        roleName = user.role
        auth_token = encode_token(user.id, roleName)
        response = {
            'status': 'success',
            'message': 'Successfully logged in',
            'authToken': auth_token
        }
        return response
    else:
        return None
    
# Save/Create New Account
@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(user_data):
    try:
        if user_data['username'] == "Failure":
            raise Exception('Failure condition triggered')
        
        with Session(db.engine) as session:
            with session.begin():
                new_user = Account(username=user_data['username'],
                                password=user_data['password'],
                                role=user_data['role'],
                                accountId=user_data['accountId'])
                session.add(new_user)
                session.commit()
            session.refresh(new_user)
            return new_user
        
    except Exception as e:
        raise e
    
# Read
def read(id):
    query = select(Account).where(id==id)
    account = db.session.execute(query).scalar_one_or_none()
    if account == None:
        raise Exception('No account found with that ID')
    return account

# Update
def update(account_data):
    query = select(Account).where(id==account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    if account == None:
        raise Exception('No account found with that ID')
    
    if account_data['password']:
        hashed_pw = bcrypt.hashpw(
            account_data['password'].encode('utf-8'),
            bcrypt.gensalt()
        )

    account.username = (account_data['username'], account.username)
    account.password = (hashed_pw, account.password)
    account.accountId = account.accountId
    db.session.commit()
    return account

# Delete/Deactivate Account
def deactivate(account_data):
    query = select(Account).where(id==account_data['id'])
    account = db.session.execute(query).scalar_one_or_none()
    if account == None:
        raise Exception('No account found with that ID')
    if account.isActive == False:
        raise Exception('Account is already deactivated')
    account.deactivate()
    return account

# Get All Accounts
def find_all():
    query = select(Account)
    accounts = db.session.execute(query).scalars().all()
    return accounts