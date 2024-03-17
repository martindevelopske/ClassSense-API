from fastapi import HTTPException,status, Depends, Request
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
    print(db.query(models.Users).filter(models.Users.id == id).first(), "prr...")
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
async def getCurrentUser(req: Request, db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        userToken = req.cookies.get("userToken")
        if not userToken:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No token attached to the request cookie. Please login to use the API")
        
        payload = jwt.decode(userToken, settings.secret_key, algorithms=[settings.algorithm])
        userId = payload.get("userId")
        userType = payload.get("userType")
        print(userId, userType)
        if userId is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Check if the user exists in the Users table
    user = db.query(models.Users).filter(models.Users.id == userId).first()
    
    # If not found, check if the user exists in the Instructors table
    if not user:
        instructor = db.query(models.Instructors).filter(models.Instructors.id == userId).first()
        if not instructor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with id: {userId} does not exist")
        return {"user": instructor, "userType": payload.get("userType")}
    
    return {"user": user, "userType": payload.get("userType")}
