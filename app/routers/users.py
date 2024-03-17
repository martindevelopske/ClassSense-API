from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import database,models, schemas
from .. import utils

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
    
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.UserOut)
async def getUser(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user