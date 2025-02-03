import jwt
import uuid
import redis
from passlib.context import CryptContext
from sqlalchemy import Select
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi import Cookie, status, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from core.config import project_settings
from core.models import User
from core.models import database_helper as db_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")

class Users_factory():

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self.session = db_helper.get_session_local
        self.oauth2_scheme = oauth2_scheme

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def jwt_encode_token(self, payload: dict, 
                         expire_minutes: int = project_settings.ACCESS_TOKEN_EXPIRE_MINUTES):
        payload_to_encode = payload.copy()
        now = datetime.utcnow()
        expire = now + timedelta(minutes=expire_minutes)
        payload_to_encode.update(
            exp=expire,
            iat=now
        )

        encoded_jwt = jwt.encode(payload=payload_to_encode, 
                                 key=project_settings.SECRET_KEY, 
                                 algorithm=project_settings.ALGORITHM)

        return encoded_jwt
    
    def jwt_decode_token(self, token: str):
        decoded_jwt = jwt.decode(token, 
                                 project_settings.SECRET_KEY, 
                                 project_settings.ALGORITHM)
        return decoded_jwt
    

    def get_current_user(self, token: str = Depends(oauth2_scheme), session: Session = Depends(db_helper.get_session_local)):
        try:
            payload = self.jwt_decode_token(token)
            email: EmailStr = payload.get("email")
            if not email:
                raise self.credentials_exception
            
            user_check_query = Select(User).where(User.email == email)
            user_info: User | None = session.execute(user_check_query).scalar_one_or_none()
            return user_info
        
        except HTTPException:
            raise self.credentials_exception
        

class Cookie_Settings():

    def __init__(self):
        self.COOKIES: dict = {}
        self.COOKIES_SESSION_ID_KEY = project_settings.COOKIES_SESSION_ID_KEY

    def generate_session_id(self) -> str:
        return uuid.uuid4().hex
    
    def get_session_data(self, session_id: str = Cookie(alias=project_settings.COOKIES_SESSION_ID_KEY)):
        if session_id not in self.COOKIES:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not Authorized"
            )
        return self.COOKIES[session_id]
    

cookie_settings = Cookie_Settings()    
users_factory = Users_factory()