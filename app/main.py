from fastapi import APIRouter, FastAPI, Request, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, sessions, instructors, auth
from .database import engine
from .config import settings
from . import models
from .utils import getCurrentUser
import time
from .middlewares.getCurrentUser import getUserMiddleware
## this line creates the tables on startup if they are not there. use alembic for updates
models.Base.metadata.create_all(bind=engine)


app= FastAPI()

allowedOrigins=["*"]


#middlewares
app.add_middleware(CORSMiddleware, allow_origins=allowedOrigins, allow_methods=["*"], allow_headers=["*"])

    
#application routes
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(instructors.router)
app.include_router(auth.router)




@app.get("/")
def test():
    return settings