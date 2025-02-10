from sqlalchemy.orm import Mapped, mapped_column
from models.admin import Admin
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

    creator: Mapped['Admin'] = db.relationship(primaryjoin='Product.createdBy == Admin.id')
    updater: Mapped['Admin'] = db.relationship(primaryjoin='Product.updatedBy == Admin.id')