from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database,schemas,utils,models,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

# @router.post("/login")
# def login(user_credentials: schemas.UserLogin,db:Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()


#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")

#     if not utils.verify(user_credentials.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")

#     access_token = oauth2.create_access_token(data= {"user_id" : user.id})

#     # return {"detail" : "Password matches succesfully!"}
#     return {"access_token" : access_token, "token_type" : "bearer"}

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data= {"user_id" : user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}