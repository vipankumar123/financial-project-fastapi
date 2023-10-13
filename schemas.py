from pydantic import BaseModel
from datetime import datetime
from typing import List
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active : bool
    full_name : str
    profile_picture : str

class UserSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active : bool

class InvestmentBase(BaseModel):
    name: str
    type: str
    quantity: float
    purchase_price: float
    current_price: Optional[float] = None
    notes: Optional[str] = None

class InvestmentCreate(InvestmentBase):
    pass

class Investment(InvestmentBase):
    id : int
    user_id: int
    purchase_date: Optional[datetime] = None

class TransactionBase(BaseModel):
    investment_id: int
    transaction_type: str
    quantity: float
    transaction_price: float
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id : int
    transaction_date: datetime


class PortfolioBase(BaseModel):
    name: str
    description: str
    investment_id: int  # Include investment_id here

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioSchema(PortfolioBase):
    id : int

class PortfolioUpdate(BaseModel):
    name: str
    description: str