from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils
from datetime import datetime, timedelta

router = APIRouter(tags=["authentication"])

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def login(userData: schemas.UserLogin, res: Response, db: Session = Depends(database.get_db)):
    try:
        # Check if the user exists
        user = db.query(models.Users).filter(models.Users.email == userData.email).first()
        if not user:
            # Check if the instructor exists
            instructor = db.query(models.Instructors).filter(models.Instructors.email == userData.email).first()
            if not instructor:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
            # Verify password for instructor
            verify = utils.verifyPassword(userData.password, instructor.password)
            if not verify:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
            # Create and return JWT token for instructor
            accessToken =  utils.createAccessToken(data={"userId": instructor.id, "userType": "instructor"})
            
            res.set_cookie(key="userToken", value=accessToken)
            return {"user": instructor, "userType": "instructor"}
        # Verify password for user
        verify = utils.verifyPassword(userData.password, user.password)
        if not verify:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        # Create and return JWT token for user
        accessToken = utils.createAccessToken(data={"userId": user.id, "userType": "student"})
        res.set_cookie(key="userToken", value=accessToken)
        return {"user":user, "userType": "student"}
    except Exception as error:
         print("something went wrong", error)

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(res: Response):
    try:

        # Clear the userToken cookie by setting its value to an empty string
        res.set_cookie(key="userToken", value="",)
        return {"message": "Logged out successfully"}
    except Exception as error:
        print(error)