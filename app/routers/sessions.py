from fastapi import APIRouter, HTTPException, status, Response, Depends, Request
from app import schemas
from sqlalchemy.orm import Session, joinedload
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
    

@router.get("/", status_code=status.HTTP_200_OK, )
async def getAllSessions(db: Session= Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    print(currentUser, "current")
    sessions = db.query(models.Sessions).all()
    if not sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no sessions in the database")

    return sessions
@router.get("/instructorSessions", status_code=status.HTTP_200_OK, )
async def getInstructorSessions(db: Session= Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    isallowed= currentUser['userType']== "instructor"
    print(isallowed, "is allow")
    print(currentUser['user'].email)
    if not isallowed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view instructor sessions.")
    
    sessions = db.query(models.Sessions).filter(models.Sessions.instructor_id== currentUser["user"].id).all()
    if not sessions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no sessions in the database")

    return sessions

@router.get("/userSessions", status_code=status.HTTP_200_OK, )
async def getUserSessions(db: Session= Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    currentUserId= currentUser["user"].id
    userSessions=[]
    queryResults= db.query(models.SessionMembers).filter(models.SessionMembers.user_id == currentUserId).all()
    if not queryResults:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"no sessions in the database")
    
    #get full details
    for session in queryResults:
        id = int(session.session_id)
        print(id, type(id))
        session, instructor = db.query(models.Sessions, models.Instructors).join(models.Instructors, models.Sessions.instructor_id == models.Instructors.id).filter(models.Sessions.id == id).first()

        print(session, instructor)
        # Extract specific attributes from session and instructor objects
        session_data = {
            "id": session.id,
            "location_id": session.location_id,
            "created_at": session.created_at,
            "name": session.name,
            "status": session.status,
        }

        instructor_data = {
            "email": instructor.email,
            # Add more attributes if needed
        }

        fullSessionDetails = {
            "session": session_data,
            "instructor": instructor_data
        }
        userSessions.append(fullSessionDetails)
        # if session, instructor:
        #     userSessions.append(fullSessionDetails)
    
   
    return userSessions


@router.post("/members", status_code=status.HTTP_200_OK )
async def addSessionMember(data: schemas.AddSessionMember, db: Session = Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):

    # try:
        print(data)
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
        if inSession is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id: {currentUserId} already in the session")
        
        newRecord= models.SessionMembers(session_id= sessionId, user_id= currentUserId)
        db.add(newRecord)
        db.commit()
        db.refresh(newRecord)
        return newRecord
    # except Exception as error:
    #      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail=f"An error occurred: {str(error)}")


@router.get("/members", status_code=status.HTTP_200_OK)
async def getSessionMembers(data: schemas.getSessionMembers, db: Session = Depends(database.get_db), currentUser= Depends(utils.getCurrentUser)):
    # try:
        sessionId= data.sessionId
      
        currentUserId= currentUser["user"].id

        #check whether user is instructor and is creator
        isallowed= currentUser['userType']== "instructor"
        if not isallowed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view session members.")
        
        #check whether session exitsts
        session = db.query(models.Sessions).filter(models.Sessions.id == sessionId).first()
        print(session)
        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Session with id: {sessionId} does not exist")
        
        #get members
        members=db.query(models.SessionMembers).filter(models.SessionMembers.session_id == sessionId).all()
        print(members)
        return members
    # except Exception as error:
    #     return f'something went woring, {error}'
    
    
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def getSession(id: int, db: Session= Depends(database.get_db)):
    session = db.query(models.Sessions).filter(models.Sessions.id == id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Session with id: {id} does not exist")

    return session
