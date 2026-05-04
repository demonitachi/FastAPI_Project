from fastapi import FastAPI
from .database import engine, SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Base, db_Product, db_seller
from .schemas import Product, displayProduct, Seller, displaySeller
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

Base.metadata.create_all(engine)

app = FastAPI(
    title="Products API",
    description="An API for managing products and sellers",
    version="1.0.0",
    redoc_url=None,
    license_info={
        "name": "MIT",
        "url": "https://fastapi.tiangolo.com/license/",
    },
    terms_of_service="https://fastapi.tiangolo.com/terms/",
    contact={
        "name": "Kunal Anand",
        "url": "https://github.com/demonitachi",
        "email": "anandkunal926@gmail.com",
    }
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/products', response_model=List[displayProduct], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    products = db.query(db_Product).all()
    return products

@app.get('/products/{id}', response_model=displayProduct, tags=["Products"])
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    return product

@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    db.delete(product)
    db.commit()
    return f'The product with id {id} has been deleted'.format(id)

@app.post('/products', status_code=status.HTTP_201_CREATED, tags=["Products"])
def add_product(request: Product, db: Session= Depends(get_db)):
    new_product = db_Product(name=request.name, description=request.description , price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put('/products/{id}', tags=["Products"])
def update_product(id: int, request: Product, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    product.name = request.name
    product.price = request.price
    product.description = request.description
    product.seller_id = 1
    db.commit()
    return f'The product with id {id} has been updated'.format(id)



@app.post('/sellers', status_code=status.HTTP_201_CREATED, response_model=displaySeller, tags=["Sellers"])
def add_sellers(request: Seller, db: Session= Depends(get_db)):
    password_hash = pwd_context.hash(request.password)
    new_seller = db_seller(username=request.username, password=password_hash , email=request.email)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller