from sqlalchemy.orm import Mapped, mapped_column
from database import db, Base
from typing import List
# import datetime

class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), nullable=False, default='user')
    isActive: Mapped[bool] = mapped_column(db.Boolean, default=True)

    # Relationships
    orders: Mapped[List['Order']] = db.relationship('Order', back_populates='customer',  foreign_keys='Order.customerId')
    products: Mapped[List['Product']] = db.relationship('Product', back_populates='creator', foreign_keys='Product.createdBy')


    def deactivate(self):
        self.isActive = False
        db.session.commit()

    def activate(self):
        self.isActive = True
        db.session.commit()