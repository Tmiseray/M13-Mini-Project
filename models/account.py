from sqlalchemy.orm import Mapped, mapped_column
from models.admin import Admin
from models.customer import Customer
from database import db, Base
from sqlalchemy import and_
import bcrypt

class Account(Base):
    __tablename__= 'Accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), nullable=False)
    accountId: Mapped[int] = mapped_column(db.Integer, nullable=False)


    admin: Mapped['Admin'] = db.relationship(
        'Admin',
        primaryjoin=and_(
            accountId == Admin.id,
            role == "admin"
            ),
        foreign_keys=[accountId],
        uselist=False,
        )

    customer: Mapped['Customer'] = db.relationship(
        'Customer',
        primaryjoin=and_(
            accountId == Customer.id,
            role == "customer"
            ),
        foreign_keys=[accountId],
        uselist=False,
        )
    
    def __init__(self, **kwargs):
        if 'password' in kwargs:
            password = kwargs['password']
            kwargs['password'] = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
        super().__init__(**kwargs)