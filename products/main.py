from fastapi import FastAPI
from .database import engine, SessionLocal
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import Base, db_Product
from .schemas import Product, displayProduct
from typing import List, Dict

Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/products')
def get_products(db: Session = Depends(get_db), response_model=list[displayProduct]):
    products = db.query(db_Product).all()
    return products

@app.get('/products/{id}')
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    return product

@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    db.delete(product)
    db.commit()
    return f'The product with id {id} has been deleted'.format(id)

@app.post('/products', status_code=status.HTTP_201_CREATED)
def add_product(request: Product, db: Session= Depends(get_db)):
    new_product = db_Product(id=request.id ,name=request.name, description=request.description , price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.put('/products/{id}')
def update_product(id: int, request: Product, db: Session = Depends(get_db)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    product.name = request.name
    product.price = request.price
    product.description = request.description
    db.commit()
    return f'The product with id {id} has been updated'.format(id)