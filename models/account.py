from sqlalchemy.orm import Mapped, mapped_column
from models.user import User
from database import db, Base
import bcrypt

class Account(Base):
    __tablename__= 'Accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), nullable=False)
    userId: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    isActive: Mapped[bool] = mapped_column(db.Boolean, default=True)

    user: Mapped['User'] = db.relationship(
        'User',
        primaryjoin=(userId == User.id),
        foreign_keys=[userId],
        uselist=False
        )
    
    def __init__(self, **kwargs):
        if 'password' in kwargs:
            password = kwargs['password']
            kwargs['password'] = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            )
        super().__init__(**kwargs)

    def deactivate(self):
        self.isActive = False
        db.session.commit()

    def activate(self):
        self.isActive = True
        db.session.commit()