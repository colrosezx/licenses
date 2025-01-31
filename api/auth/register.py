from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import Select, Update
from pydantic import EmailStr
from .passwords_factory import users_factory
from .schemas import UserCreate
from core.models import User
from core.models import database_helper as db_helper
