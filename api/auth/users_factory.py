from passlib.context import CryptContext
from sqlalchemy import Select
from sqlalchemy.orm import Session
from pydantic import EmailStr
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from core.config import project_settings
from core.models import User
from core.models import database_helper as db_helper
from .schemas import UserLogin

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
        
    
    
users_factory = Users_factory()