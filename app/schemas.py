from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str


class InstructorCreate(BaseModel):
    email: str
    password: str


class InstructorOut(BaseModel):
    email: str
    created_at: datetime

    class Config: 
        orm_mode: True


class UserOut(BaseModel):
    email: str
    created_at: datetime

    class Config: 
        orm_mode: True

class SessionCreate(BaseModel):
    name: str

    status: str

class AddSessionMember(BaseModel):
    sessionId: int
class deleteAttendanceRecord(BaseModel):
    studentId: int
    sessionId: int
class getSessionMembers(BaseModel):
    sessionId: int

class SessionOut(BaseModel):
    name: str
    instructor_id: int
    location_id: int
    status: str

    class Config: 
        orm_mode: True
