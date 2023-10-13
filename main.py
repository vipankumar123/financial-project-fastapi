from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models import User
from schemas import UserSchema
from typing import List
from accounts import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Security
from accounts.api import get_current_user
from accounts.api import get_user_by_username
from apis import investment, transaction, portfolio

app = FastAPI()

create_tables()

app.include_router(auth.auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(investment.router, prefix="/api", tags=["Investment API's"]) 
app.include_router(transaction.transaction_router, prefix="/api", tags=["Transaction API's"]) 
app.include_router(portfolio.portfolio_router, prefix="/api", tags=["Portfolio API's"]) 



# @app.get("/users/", response_model=List[UserSchema], tags=["Authentication"])
# def get_all_users(db: Session = Depends(get_db), user: User = Security(get_current_user, scopes=["read"])):
#     users = db.query(User).all()
#     return users

# # Define the route to get a user by ID
# @app.get("/users/{user_id}", response_model=UserSchema, tags=["Authentication"])
# def get_user_by_id(user_id: int, db: Session = Depends(get_db), user: User = Security(get_current_user)):
#     # Retrieve the user from the database by user_id
#     user = db.query(User).filter(User.id == user_id).first()
    
#     # Check if the user exists
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     # Return the user as a response
#     return user



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    #http://localhost:8000/docs
