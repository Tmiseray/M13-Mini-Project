from sqlalchemy.orm import Mapped, mapped_column
from models.order import Order
from database import db, Base
from typing import List
import datetime

class Customer(Base):
    __tablename__ = 'Customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    role: Mapped[str] = mapped_column(db.String(10), nullable=False, default='customer')

    orders: Mapped[List['Order']] = db.relationship(back_populates='customer')