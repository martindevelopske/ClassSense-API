from fastapi import APIRouter, HTTPException, status, Response, Depends
from app import schemas
from sqlalchemy.orm import Session
from .. import database

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(user_data: schemas.UserCreate, db: Session = Depends(database.get_db) ):
    return user_data
