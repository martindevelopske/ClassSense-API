from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .. import database,models, schemas
from .. import utils

router = APIRouter(prefix="/attendance", tags=["Attendance"] )


#add attendance
@router.post("/add", status_code=status.HTTP_200_OK)
async def addAttendance(data: schemas.getSessionMembers, db: Session = Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    try:

        sessionId= data.sessionId
        currentUserId= currentUser["user"].id
        #check whether user is student
        isallowed= currentUser['userType']== "student"
        if not isallowed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to join a sessions.")
        #check whether session exitsts
        session = db.query(models.Sessions).filter(models.Sessions.id== sessionId).first()
        print(session)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Session with id: {sessionId} does not exist")
        #check whether the user is already in the sesion
        inSession=db.query(models.SessionMembers).filter((models.SessionMembers.user_id == currentUserId) &  (models.SessionMembers.session_id == sessionId)).first()
        print(inSession)
        if not inSession:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id: {currentUserId} is not registered for this session")
        #check if similar record exists
        exists= db.query(models.Attendance).filter((models.Attendance.session_id == sessionId) & (models.Attendance.user_id==currentUserId)).first()
        if exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"record already in the database")

        #add new attendance record
        newAttendance= models.Attendance(user_id=currentUserId, session_id=sessionId)
        db.add(newAttendance)
        db.commit()
        db.refresh(newAttendance)
        return newAttendance
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong, {error}")


#get session attendance
@router.get("/attendees", status_code=status.HTTP_200_OK)
async def addAttendance(data: schemas.getSessionMembers, db: Session = Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    try:
        sessionId= data.sessionId
        #check if current user is an instructor-from current user
        isallowed= currentUser['userType']== "instructor"
        print(isallowed, "is allow")
        print(currentUser['user'].email)
        if not isallowed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view session attendees.")
        
        #check if similar record exists
        records= db.query(models.Attendance).filter(models.Attendance.session_id == sessionId).all()
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No attendees for session with id {sessionId}")
        return records
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong, {error}")
    


#remove attendace