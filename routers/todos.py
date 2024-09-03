from fastapi import APIRouter,Depends,HTTPException,status,Path
from pydantic import BaseModel,Field
from models import Todos
from datbase import SessionLocal
from sqlalchemy.orm import Session
router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    desc: str = Field(min_length=3, max_length=50)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get('/')
async def get_all(db: Session = Depends(get_db)):
    return db.query(Todos).all()

#get partical record
@router.get('/todo/{todo_id}')
async def read_todo(todo_id:int=Path(gt=0),
                    db: Session = Depends(get_db),
                    status_code=status.HTTP_200_OK):
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(404,'todo not found')

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request:TodoRequest,db: Session = Depends(get_db)):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_request: TodoRequest,
                      todo_id: int = Path(gt=0),
                      db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(404,'todo not found')
    todo_model.title = todo_request.title
    todo_model.desc = todo_request.desc
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete('/todo/{todo_id}',status_code=status.HTTP_200_OK)
async def delete(todo_id: int = Path(gt=0),
                        db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(404,'todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()