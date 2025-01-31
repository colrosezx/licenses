from fastapi import APIRouter, HTTPException, status, Depends, Query
from passlib.context import CryptContext
from sqlalchemy import Select, Update
from sqlalchemy.orm import Session
from pydantic import EmailStr
from .passwords_factory import password_factory
from .schemas import UserCreate, UserLogin
from core.models import User
from core.models import database_helper as db_helper


router = APIRouter(prefix="/auth", tags=['Authentification'])

def get_session_local():
    yield db_helper.sessionmaker()

@router.post("/register/")
def user_register(
    user: UserCreate, 
    session: Session = Depends(get_session_local)
):
    user_reg_query = Select(User).where(User.email == user.email)
    user_info: User | None = session.execute(user_reg_query).scalar_one_or_none()   

    if user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    elif user.password != user.re_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords"
        )   
      
    else:
        creation_user = User(
            email=user.email,
            password=password_factory.get_password_hash(user.password)
        )

        session.add(creation_user)
        session.commit()

    return {"message": "User registered successfully"}

@router.post("/login/")
def login_user(
    user: UserLogin, 
    session: Session = Depends(get_session_local)
):
    




