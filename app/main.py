from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, sessions
from .database import engine
from .config import settings
from . import models


models.Base.metadata.create_all(bind=engine)


app= FastAPI()

allowedOrigins=["*"]


#middlewares
app.add_middleware(CORSMiddleware, allow_origins=allowedOrigins, allow_methods=["*"], allow_headers=["*"])
#application routes
app.include_router(users.router)




@app.get("/")
def test():
    return settings