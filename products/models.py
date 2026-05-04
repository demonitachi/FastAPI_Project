from sqlalchemy import Column, Integer, String, Float
from .database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class db_Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    Seller = relationship("db_seller", back_populates="Products")

class db_seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    Products = relationship("db_Product", back_populates="Seller")