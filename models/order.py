from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import event
from models.product import Product
from models.customer import Customer
import datetime

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    customerId: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'), nullable=False)
    productId: Mapped[int] = mapped_column(db.ForeignKey('Products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    totalPrice: Mapped[float] = mapped_column(db.Float, nullable=False)
    orderPlaced: Mapped[datetime.datetime] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    updatedOn: Mapped[datetime.datetime] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    customer: Mapped['Customer'] = db.relationship(back_populates='orders')
    product: Mapped['Product'] = db.relationship(primaryjoin='Order.productId == Product.id')
    

@event.listens_for(Order, 'before_commit')
def total_price(mapper, connection, target):
    if target.productId:
        product = db.session.get(Product, target.productId)
        if product:
            target.totalPrice = round((target.quantity * product.price), 2)

@event.listens_for(Order, 'before_update')
def update_total_price(mapper, connection, target):
    if target.productId:
        product = db.session.get(Product, target.productId)
        if product:
            target.totalPrice = round((target.quantity * product.price), 2)