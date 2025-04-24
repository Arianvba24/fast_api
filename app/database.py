from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings

settings = Settings()

# En esta variable lo que hacemos es poner el nombre de usuario, contraseña, dirección y/o puerto y el nombre del servidor 
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Creamos el motor
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos la sesión
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()