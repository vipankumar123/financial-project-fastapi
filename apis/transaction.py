from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import models
import schemas
from typing import List
from database import SessionLocal
from accounts.api import get_current_user
import datetime

transaction_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@transaction_router.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["create"]),
):
    # Check if the investment exists and belongs to the user
    db_investment = db.query(models.Investment).filter(
        models.Investment.id == transaction.investment_id,
        models.Investment.user_id == user["id"],  # Ensure the investment belongs to the user
    ).first()
    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found!!")

    # Create the transaction and associate it with the user
    db_transaction = models.Transaction(
        user_id=user["id"],  # Associate the transaction with the user
        investment_id=transaction.investment_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        transaction_price=transaction.transaction_price,
        notes=transaction.notes,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


@transaction_router.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction_by_id(
    transaction_id: int,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["transaction"]),  # Require authentication
):
    # Retrieve and validate the transaction
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Ensure that the user can access this transaction (authorization)
    db_transaction_user = db.query(models.Transaction).filter(models.Transaction.id == transaction_id, models.Transaction.user_id == user["id"]).first()

    if not db_transaction_user:
        raise HTTPException(status_code=403, detail="You are not authorized to access this transaction")
    
    return db_transaction

@transaction_router.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: models.User = Security(get_current_user, scopes=["transaction"]),  # Require authentication
):
    try:
        # Retrieve and return transactions associated with the authenticated user
        transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user["id"]).offset(skip).limit(limit).all()
        return transactions
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=500, detail="Read transactions failed")