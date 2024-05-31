from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from datetime import date

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(150))
    birthday: Mapped[str] = mapped_column(String(150))
    other: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    user: Mapped['User'] = relationship(argument='User', backref='contacts', lazy='joined')
    
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    