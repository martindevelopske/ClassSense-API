from fastapi import HTTPException,status, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from .config import settings
from . import database, models

pwd_context=CryptContext(schemes=['bcrypt'], deprecated='auto')
#password actions
def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def getPasswordHash(password):
    return pwd_context.hash(password)

def createAccessToken(data: dict):
    to_encode= data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=settings.access_key_expiry)
    to_encode.update({"exp": expire})

    encoded_token=jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_token

async def getUser(id: int,  db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
async def getCurrentUser(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("getting current user on this request..................")
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        userId: str = payload.get("userId")
        if userId is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user = getUser(id=userId)
    if user is None:
        raise credentials_exception
    return user

