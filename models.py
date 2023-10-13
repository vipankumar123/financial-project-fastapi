
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base

# Define the association table for the many-to-many relationship between portfolios and investments
portfolio_investment_association = Table(
    'portfolio_investment_association',
    Base.metadata,
    Column('portfolio_id', Integer, ForeignKey('portfolio.id')),
    Column('investment_id', Integer, ForeignKey('investment.id'))
)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    profile_picture = Column(String)

    investments = relationship('Investment', back_populates='user')
    portfolios = relationship('Portfolio', back_populates='user')  
    transactions = relationship('Transaction', back_populates='user')



class Investment(Base):
    __tablename__ = 'investment'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_price = Column(Float)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='investments')
    transactions = relationship('Transaction', back_populates='investment')
    portfolios = relationship('Portfolio', secondary=portfolio_investment_association, back_populates='investments')

class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Added user_id field
    investment_id = Column(Integer, ForeignKey('investment.id'), nullable=False)
    transaction_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    transaction_price = Column(Float, nullable=False)
    notes = Column(String)

    user = relationship('User', back_populates='transactions')
    investment = relationship('Investment', back_populates='transactions')

class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    investment_id = Column(Integer, ForeignKey('investment.id'))
    
    user = relationship('User', back_populates='portfolios')
    investments = relationship('Investment', secondary=portfolio_investment_association, back_populates='portfolios')
