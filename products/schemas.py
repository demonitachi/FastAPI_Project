from pydantic import BaseModel


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




