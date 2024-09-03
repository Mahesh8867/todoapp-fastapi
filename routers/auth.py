from fastapi import APIRouter,status,Depends
from datbase import SessionLocal
from models import Users
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
router = APIRouter()
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request:CreateUserRequest,db: Session = Depends(get_db)):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()

