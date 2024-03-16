from fastapi import HTTPException, status, Request
from ..utils import getCurrentUser

async def getUserMiddleware(req:Request, call_next):
    
    token= req.cookies.get("userToken")
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No token attached to the request cookie. Please login to use the API")
    currentUser=getCurrentUser(token)
    response= await call_next(req)
    return response