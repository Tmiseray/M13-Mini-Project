from sqlalchemy.orm import Mapped, mapped_column, relationship
# from models.admin import Admin
from database import db, Base
import datetime

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    createdBy: Mapped[int] = mapped_column(db.ForeignKey('Admins.id'), nullable=False)
    createdAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    updatedBy: Mapped[int] = mapped_column(db.ForeignKey('Admins.id'), nullable=True)
    updatedAt: Mapped[datetime.date] = mapped_column(db.Date, nullable=False, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    isActive: Mapped[bool] = mapped_column(db.Boolean, default=True)

    # Relationship
    admin: Mapped['User'] = db.relationship('User', back_populates='products')
    creator: Mapped['User'] = db.relationship(primaryjoin='Product.createdBy == User.id')
    updater: Mapped['User'] = db.relationship(primaryjoin='Product.updatedBy == User.id')


    def deactivate(self):
        self.isActive = False
        db.session.commit()

    def activate(self):
        self.isActive = True
        db.session.commit()