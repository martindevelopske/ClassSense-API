from fastapi import APIRouter, HTTPException, status, Response
from app import schemas


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createUser(user_data: schemas.UserCreate ):
    return user_data
