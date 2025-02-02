from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    re_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

