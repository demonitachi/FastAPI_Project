from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str = None



class displayProduct(BaseModel):
    id: int
    name: str
    description: str = None
    class Config:
        orm_mode = False