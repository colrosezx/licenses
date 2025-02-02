from passlib.context import CryptContext
from pydantic import EmailStr
import jwt
from datetime import datetime, timedelta
from core.config import project_settings

class Users_factory():

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def jwt_encode_token(self, payload: dict):
        payload_to_encode = payload.copy()
        payload_to_encode.update(
            {"exp": datetime.utcnow() + timedelta(minutes=project_settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
        )

        encoded_jwt = jwt.encode(payload=payload_to_encode, 
                                 key=project_settings.SECRET_KEY, 
                                 algorithm=project_settings.ALGORITHM,
                                 type="Bearer")

        return encoded_jwt
    
    def jwt_decode_token(self, payload: dict):
        decoded_jwt = jwt.decode(payload=payload, 
                                 key=project_settings.SECRET_KEY, 
                                 algorithm=project_settings.ALGORITHM,
                                 type="Bearer")
        return decoded_jwt


    
    
users_factory = Users_factory()