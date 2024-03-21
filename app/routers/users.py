from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import database,models, schemas
from .. import utils
from ..config import settings
from jose import jwt, JWTError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(userData: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        userDataDict=userData.model_dump()
        #check existing user
        user = db.query(models.Users).filter(models.Users.email == userDataDict["email"]).first()
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with that email already exists")


        userDataDict['password']= utils.getPasswordHash(userDataDict["password"])
        # newUser= models.Users(**userDataDict)
        newUser= models.Users(email=userDataDict["email"], password=userDataDict['password'])
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        #assing user the student role
        newRole= models.UserRoles(user_id=newUser.id, role_id=1)
        return newUser
    except SQLAlchemyError as error:
        return error

@router.get("/currentUser", status_code=status.HTTP_200_OK)
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
    
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.UserOut)
async def getUser(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user
