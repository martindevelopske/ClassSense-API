from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models,schemas, database
from .. import utils

router= APIRouter( tags=["authentication"])

@router.post("/login", response_model=schemas.UserOut, status_code=status.HTTP_200_OK)
async def login(userData: schemas.UserLogin, res: Response, db: Session= Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == userData.email).first()
    # print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    verify= utils.verifyPassword(userData.password, user.password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create and return jwt token
    accessToken= utils.createAccessToken(data={"userId": user.id})

    # set the response cookie
    res.set_cookie(key="userToken", value=accessToken)
    return user

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(res: Response):
    res.set_cookie(key="userToken", value="")