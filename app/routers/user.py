from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import engine,get_db

router = APIRouter(

    prefix="/users",
    tags=["Users"]
)



@router.get("/{id}")
def get_user(id : int,db : Session = Depends(get_db)):

    post = db.query(models.User).filter(models.User.id == id).first()

    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} does not exist")

    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user