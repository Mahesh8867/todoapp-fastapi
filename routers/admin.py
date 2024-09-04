from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,status,Path
from ..models import Todos
from ..datbase import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


user_dependency= Annotated[dict,Depends(get_current_user)]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/todo',status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: Session = Depends(get_db)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(401,'auth failed')
    return db.query(Todos).all()
@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db: Session = Depends(get_db),todo_id:int = Path(gt=0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(401, 'auth failed')
    todo_model = db.query(Todos).filter(Todos.id ==todo_id).first()
    if todo_model is None:
        raise HTTPException(404,'todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()