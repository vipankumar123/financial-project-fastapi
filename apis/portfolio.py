from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from schemas import PortfolioCreate, PortfolioSchema, PortfolioUpdate
from models import Portfolio as PortfolioModel
from accounts.api import get_current_user
from typing import List
from database import SessionLocal
from models import User, Portfolio, Investment

portfolio_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@portfolio_router.post("/portfolios/", response_model=PortfolioSchema)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["create"]),
):
    
    # Check if the specified investment_id belongs to the authenticated user
    db_investment = db.query(Investment).filter(
        Investment.id == portfolio.investment_id,
        Investment.user_id == user["id"],
    ).first()

    if db_investment is None:
        raise HTTPException(status_code=404, detail="Investment not found or does not belong to the user.")

    # Create a Portfolio instance without specifying investment_id
    db_portfolio = PortfolioModel(**portfolio.dict(), user_id=user["id"])

    # Add the portfolio to the database session and commit
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)

    # Return the created portfolio
    return db_portfolio


@portfolio_router.get("/portfolios/{portfolio_id}", response_model=PortfolioSchema)
def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["read"]),
):
    # Query the portfolio by ID and verify that it belongs to the authenticated user
    db_portfolio = db.query(PortfolioModel).filter(
        PortfolioModel.id == portfolio_id,
        PortfolioModel.user_id == user["id"],
    ).first()

    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found or does not belong to the user.")

    return db_portfolio


@portfolio_router.get("/portfolios/", response_model=List[PortfolioSchema])
def read_portfolios(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["read"]),
):
    # Query the portfolios that belong to the authenticated user
    portfolios = db.query(PortfolioModel).filter(PortfolioModel.user_id == user["id"]).offset(skip).limit(limit).all()
    return portfolios


@portfolio_router.put("/portfolios/{portfolio_id}", response_model=PortfolioSchema)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,  # Renamed to portfolio_update
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["edit"]),
):
    db_portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    if db_portfolio.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this portfolio")
    
    for key, value in portfolio_update.dict().items():
        setattr(db_portfolio, key, value)

    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@portfolio_router.delete("/portfolios/{portfolio_id}", response_model=PortfolioSchema)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["delete"]),
):
    db_portfolio = db.query(PortfolioModel).filter(PortfolioModel.id == portfolio_id).first()
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    if db_portfolio.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this portfolio")

    db.delete(db_portfolio)
    db.commit()
    return db_portfolio
