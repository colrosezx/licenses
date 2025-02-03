from typing import Optional
from fastapi import APIRouter, HTTPException, Response, status, Depends, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import Select, Update
from sqlalchemy.orm import Session
from pydantic import EmailStr
from .users_factory import users_factory, cookie_settings
from .schemas import UserCreate, UserLogin
from core.models import User
from core.models import database_helper as db_helper
from core.config import project_settings

router = APIRouter(prefix="/auth", tags=['Authentification'])

@router.post("/register/")
def user_register(
    user: UserCreate, 
    session: Session = Depends(db_helper.get_session_local)
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
            password=users_factory.get_password_hash(user.password)
        )

        session.add(creation_user)
        session.commit()
        access_token = users_factory.jwt_encode_token(payload={"sub": creation_user.id, "email": creation_user.email, "status": creation_user.status})

    return {"message": "User registered successfully", "access_token": access_token, "token_type": "bearer"}

@router.post("/login/")
def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db_helper.get_session_local)
):
    user_check_query = Select(User).where(User.email == form_data.username)
    user_info: User | None = session.execute(user_check_query).scalar_one_or_none()

    if user_info:
        hashed_password_from_db = user_info.password
     
        if users_factory.verify_password(form_data.password, hashed_password_from_db):

            access_token = users_factory.jwt_encode_token(payload={"sub": str(user_info.id), 
                                                                   "email": user_info.email, 
                                                                   "status": user_info.status})
            session_id = cookie_settings.generate_session_id()
            cookie_settings.COOKIES[session_id] = {"user": user_info}
            response.set_cookie(key=cookie_settings.COOKIES_SESSION_ID_KEY, 
                                       value=session_id,
                                       httponly=True,
                                       max_age=3600,
                                       path="/")
            print(cookie_settings.COOKIES)
            return {"message": "User login successfully", "access_token": access_token, "token_type": "bearer"}
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="False password")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not registred")



@router.get('/users/profile/')
def check_cookie(
    user_session_data_from_session: dict = Depends(cookie_settings.get_session_data)
):
    user = user_session_data_from_session["user"]
    return {
        f"Hello, {user.email}!"
 }

@router.get('/logout-cookie')
def logout(
    response: Response,
    session_id: Optional[str] = Cookie(default=None, alias=project_settings.COOKIES_SESSION_ID_KEY),
    user_session_data: str = Depends(cookie_settings.get_session_data)
):

    cookie_settings.COOKIES.pop(session_id)
    response.delete_cookie(cookie_settings.COOKIES_SESSION_ID_KEY)
    user = user_session_data["user"]

    return {
        f"Bye, {user}!"
    }