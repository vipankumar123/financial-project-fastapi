from fastapi import APIRouter,Depends
from .api import *
import schemas
from database import SessionLocal
from fastapi import File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import File, UploadFile, Form
from pydantic import EmailStr


auth_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/api/register", tags=["Authentication"])
def register_user(
    username: str = Form(...),
    email: EmailStr = Form(...),
    hashed_password: str = Form(...),
    is_active: bool = Form(...),
    full_name: str = Form(...),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        db_user = get_user_by_username(db, username=username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        if profile_picture:
            file_extension = profile_picture.filename.split('.')[-1]
            unique_filename = f"{username}.{file_extension}"
            save_path = f"profile_pictures/{unique_filename}"  # Update this path
            with open(save_path, "wb") as f:
                f.write(profile_picture.file.read())
            user = schemas.UserCreate(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=is_active,
                full_name=full_name,
                profile_picture=save_path,
            )
        else:
            user = schemas.UserCreate(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=is_active,
                full_name=full_name,
            )
        db_user = create_user(db=db, user=user)
        return db_user
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=500, detail="Registration failed")



@auth_router.post("/api/login", tags=["Authentication"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username not found!!")
    if verify_password(form_data.password, db_user.hashed_password):
        token = create_access_token(db_user)
        return {"token": token, "token_type": "bearer"}
    return HTTPException(status_code=400, detail="password not matched!!")
