from fastapi import APIRouter, FastAPI, Request, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, sessions, instructors, auth, attendance
from .database import engine
from .config import settings
from . import models
from .utils import getCurrentUser
import time
## this line creates the tables on startup if they are not there. use alembic for updates
models.Base.metadata.create_all(bind=engine)
# metadata = models.Base.metadata

# metadata.drop_all(bind=engine)
# metadata.create_all(bind=engine)

app= FastAPI()

allowedOrigins=["http://localhost","http://127.0.0.1", 'http://localhost:5173']


#middlewares
app.add_middleware(CORSMiddleware, allow_origins=allowedOrigins, allow_methods=["*"], allow_headers=["*"], allow_credentials=True, expose_headers=["*"])

    
#application routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(instructors.router)
app.include_router(sessions.router)
app.include_router(attendance.router)




@app.get("/")
def test():
    return settings