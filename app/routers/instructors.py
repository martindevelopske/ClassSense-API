from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import database,models, schemas
from .. import utils

router = APIRouter(prefix="/instructors", tags=["instructors"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createInstructor(user_data: schemas.InstructorCreate, db: Session = Depends(database.get_db) ):
    try:
        instructorDataDict=user_data.model_dump()

         #check existing user
        user = db.query(models.Instructors).filter(models.Users.email == instructorDataDict["email"]).first()
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Instructor with that email already exists")

        instructorDataDict['password']= utils.getPasswordHash(instructorDataDict["password"])
        newInstructor= models.Instructors(**instructorDataDict)
        db.add(newInstructor)
        db.commit()
        db.refresh(newInstructor)
        print("new id", newInstructor.id)
        defaultRole= models.UserRoles(instructor_id= newInstructor.id, role_id=2)
        db.add(defaultRole)
        db.commit()
        db.refresh(newInstructor)
        # add role to the instructor
        return newInstructor
    except SQLAlchemyError as error:
        return error
    
@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.InstructorOut)
async def getInstructor(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.Instructors).filter(models.Instructors.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user