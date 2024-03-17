from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .. import database,models, schemas
from .. import utils

router = APIRouter(prefix="/sessions", tags=["Sessions"] )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createSession(session_data: schemas.SessionCreate, db: Session = Depends(database.get_db) ,currentUser= Depends(utils.getCurrentUser)):
    try:
        #check if current user is an instructor-from current user
        isallowed= currentUser['userType']== "instructor"
        print(isallowed, "is allow")
        print(currentUser['user'].email)
        if not isallowed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to create sessions.")
        sessionDataDict=session_data.model_dump()
        sessionDataDict['instructor_id']=currentUser['user'].id
        newSession= models.Sessions(**sessionDataDict)
        print("------------", newSession)
        db.add(newSession)  
        db.commit()
        db.refresh(newSession)
        return newSession
    except (SQLAlchemyError, IntegrityError) as error:
        if IntegrityError: 
            return "integrity error"
        return error
    

@router.get("/", status_code=status.HTTP_302_FOUND, )
async def getAllSessions(db: Session= Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    print(currentUser, "current")
    sessions = db.query(models.Sessions).all()
    if not sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no sessions in the database")

    return sessions


@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.SessionOut)
async def get_session(id: int, db: Session= Depends(database.get_db)):
    session = db.query(models.Sessions).filter(models.Sessions.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session with id: {id} does not exist")

    return session