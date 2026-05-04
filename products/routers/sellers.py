from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import db_seller
from ..schemas import Seller, displaySeller
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

routers = APIRouter()

@routers.post('/sellers', status_code=status.HTTP_201_CREATED, response_model=displaySeller, tags=["Sellers"])
def add_sellers(request: Seller, db: Session= Depends(get_db)):
    password_hash = pwd_context.hash(request.password)
    new_seller = db_seller(username=request.username, password=password_hash , email=request.email)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller