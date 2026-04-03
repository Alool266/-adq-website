from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from .. import database, models, auth
from ..database import get_db

router = APIRouter()

class AdminCreate(BaseModel):
    username: str
    email: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = auth.authenticate_admin(db, username=form_data.username, password=form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create", response_model=AdminResponse)
def create_admin(admin_data: AdminCreate, db: Session = Depends(get_db), current_admin: models.Admin = Depends(auth.get_current_admin)):
    """Create a new admin (requires admin authentication)"""
    db_admin = db.query(models.Admin).filter(models.Admin.username == admin_data.username).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = auth.get_password_hash(admin_data.password)
    new_admin = models.Admin(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=hashed_password
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.get("/me", response_model=AdminResponse)
def get_current_admin_info(current_admin: models.Admin = Depends(auth.get_current_admin)):
    return current_admin
