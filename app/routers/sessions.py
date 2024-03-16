from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .. import database,models, schemas
from .. import utils
from app.middlewares.getCurrentUser import getUserMiddleware

router = APIRouter(prefix="/sessions", tags=["Sessions"], dependencies=[Depends(getUserMiddleware)])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SessionOut)
async def createSession(session_data: schemas.SessionCreate, db: Session = Depends(database.get_db) ):
    try:
        session_data_dict=session_data.model_dump()
        new_session= models.Sessions(**session_data_dict)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    except (SQLAlchemyError, IntegrityError) as error:
        return error
    

@router.get("/", status_code=status.HTTP_302_FOUND, )
async def getAllSessions(db: Session= Depends(database.get_db)):
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