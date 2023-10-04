from sqlalchemy import Column, Text, Integer, ForeignKey, Boolean, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    email = Column(String(200), unique=True)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    product = relationship("Product", back_populates="user")


    def __repr__(self):
        return f"{self.username}"



class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)




class Product(Base):

    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    old_price = Column(Integer, nullable=False)
    new_price = Column(Integer, nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref="product")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='product')



