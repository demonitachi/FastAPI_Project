from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    name: str
    price: float
    description: str = None

class Seller(BaseModel):
    username: str
    email: str
    password: str

class displaySeller(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True


class displayProduct(BaseModel):
    name: str
    price: float
    description: str = None
    Seller: displaySeller
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

