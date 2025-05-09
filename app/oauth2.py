from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import Settings

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str,credentials_exception):

    try:
  
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
     
        id_value : str = payload.get("user_id")

        if id_value is None:
            raise credentials_exception
        token_data = schemas.TokenData(id_value=str(id_value))

    except JWTError:
        raise credentials_exception

    return token_data

   


def get_current_user(token: str = Depends(oauth2_scheme),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not valid credentials",headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id_value).first()

    return user


# def get_current_user(token: str = Depends(oauth2_scheme)):

#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not valid credentials",headers={"WWW-Authenticate" : "Bearer"})

#     return verify_access_token(token,credentials_exception)