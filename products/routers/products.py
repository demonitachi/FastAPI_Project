from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import db_Product
from ..schemas import Product, displayProduct
from typing import List
from ..routers.login import get_current_user
from ..schemas import displaySeller, Seller

routers = APIRouter()


@routers.get('/products', response_model=List[displayProduct], tags=["Products"])
def get_products(db: Session = Depends(get_db), current_user: Seller = Depends(get_current_user)):
    products = db.query(db_Product).all()
    return products

@routers.get('/products/{id}', response_model=displayProduct, tags=["Products"])
def get_product(id: int, db: Session = Depends(get_db), current_user: Seller = Depends(get_current_user)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    return product

@routers.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(id: int, db: Session = Depends(get_db), current_user: Seller = Depends(get_current_user)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    db.delete(product)
    db.commit()
    return f'The product with id {id} has been deleted'.format(id)

@routers.post('/products', status_code=status.HTTP_201_CREATED, tags=["Products"])
def add_product(request: Product, db: Session= Depends(get_db), current_user: Seller = Depends(get_current_user)):
    new_product = db_Product(name=request.name, description=request.description , price=request.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@routers.put('/products/{id}', tags=["Products"])
def update_product(id: int, request: Product, db: Session = Depends(get_db), current_user: Seller = Depends(get_current_user)):
    product = db.query(db_Product).filter(db_Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'The product with id {id} does not exist'.format(id))
    product.name = request.name
    product.price = request.price
    product.description = request.description
    product.seller_id = 1
    db.commit()
    return f'The product with id {id} has been updated'.format(id)