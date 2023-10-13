from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
import models
from typing import List
from database import SessionLocal
from fastapi import Depends, HTTPException, status, Security
from accounts.api import get_current_user
from models import User
import datetime

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/investments/", response_model=schemas.Investment)
def create_investment(
    investment: schemas.InvestmentCreate,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["create"]),
):
    user_id = user["id"]
    db_investment = models.Investment(user_id=user_id,**investment.dict())
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)

    return db_investment

@router.get("/investments/{investment_id}", response_model=schemas.Investment)
def read_investment(
    investment_id: int,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["read"]),  # Add authentication
):
    # Filter investments by user_id and investment_id
    db_investment = db.query(models.Investment).filter(
        models.Investment.id == investment_id, models.Investment.user_id == user["id"]).first()
    
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found")
    
    return db_investment

@router.get("/investments/", response_model=List[schemas.Investment])
def read_investments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["read"]),  # Add authentication
):
    # Filter investments by user_id
    investments = db.query(models.Investment).filter(models.Investment.user_id == user["id"]).offset(skip).limit(limit).all()
    
    return investments


@router.put("/edit/investments/{investment_id}", response_model=schemas.Investment)
def edit_investment(
    investment_id: int,
    investment_data: schemas.InvestmentCreate,  # Use InvestmentEdit schema for editing
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["edit"]),  # Require authentication and authorization
):
    # Check if the investment exists
    db_investment = db.query(models.Investment).filter(models.Investment.id == investment_id).first()
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found!!")
    
    db_investment_user = db.query(models.Investment).filter(models.Investment.id == investment_id, models.Investment.user_id == user["id"]).first()
    if db_investment_user is None:
        raise HTTPException(status_code=404, detail="You are not Authorize to edit this user!!")

    # Update the investment fields
    db_investment.name = investment_data.name
    db_investment.type = investment_data.type
    db_investment.quantity = investment_data.quantity
    db_investment.purchase_price = investment_data.purchase_price
    db_investment.current_price = investment_data.current_price
    db_investment.notes = investment_data.notes

    db.commit()
    db.refresh(db_investment)

    return db_investment
