from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import database,models, schemas
from .. import utils

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createUser(user_data: schemas.UserCreate, db: Session = Depends(database.get_db) ):
    try:
        user_data_dict=user_data.model_dump()
        user_data_dict['password']= utils.get_password_hash(user_data_dict["password"])
        new_user= models.User(**user_data_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as error:
        return error
    
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.UserOut)
async def getUser(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user