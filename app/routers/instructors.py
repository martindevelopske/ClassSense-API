from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import database,models, schemas
from .. import utils

router = APIRouter(prefix="/instructors", tags=["instructors"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InstructorOut)
async def createInstructor(user_data: schemas.InstructorCreate, db: Session = Depends(database.get_db) ):
    try:
        instructor_data_dict=user_data.model_dump()
        instructor_data_dict['password']= utils.get_password_hash(instructor_data_dict["password"])
        new_instructor= models.Instructors(**instructor_data_dict)
        db.add(new_instructor)
        db.commit()
        db.refresh(new_instructor)
        return new_instructor
    except SQLAlchemyError as error:
        return error
    
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.InstructorOut)
async def getInstructor(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.Instructors).filter(models.Instructors.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user