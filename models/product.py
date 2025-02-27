from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import db, Base
import datetime

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    createdBy: Mapped[int] = mapped_column(db.ForeignKey('Users.id'), nullable=False)
    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    updatedBy: Mapped[int] = mapped_column(db.ForeignKey('Users.id'), nullable=True)
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    isActive: Mapped[bool] = mapped_column(db.Boolean, default=True)

    # Relationship
    creator: Mapped['User'] = db.relationship('User', foreign_keys=[createdBy])
    updater: Mapped['User'] = db.relationship('User', foreign_keys=[updatedBy])
    orders: Mapped['Order'] = db.relationship('Order', back_populates='product')


    def deactivate(self):
        self.isActive = False
        db.session.commit()

    def activate(self):
        self.isActive = True
        db.session.commit()