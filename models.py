from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String(25),unique=True)
    email = Column(String(70),unique=True)
    password = Column(Text,nullable=True)
    is_staff = Column(Boolean,default=False)
    is_active = Column(Boolean,default=False)
    orders = Relationship("Order",back_populates="user") #one to many relationship

    def __repr__(self):
        return f'<user {self.username}'

class Order(Base):
    __tablename__ = "orders"
    ORDER_STATUS = (
        ('PENDING','pending'),
        ('IN_TRANSIT','in_transit'),
        ('DELIVERED','delivered')
    )
    id = Column(Integer,primary_key=True)
    quantity = Column(Integer,nullable=False)
    order_statuses = Column(ChoiceType(choices=ORDER_STATUS),default="PENDING")
    user_id = Column(Integer,ForeignKey("user.id"))
    user = Relationship('User',back_populates='orders') #many to one relationship
    product_id = Column(Integer, ForeignKey('product.id'))
    product = Relationship('Product',back_populates='orders') #many to one relationship
  
    def __repr__(self):
        return f'<Order {self.id}'

class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer,primary_key=True)
    name = Column(String(100))
    price = Column(Integer)

    def __repr__(self):
        return f'<Product {self.name}'