from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union



class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str

class Instructor(BaseModel):
    id: int
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class InstructorCreate(BaseModel):
    email: str
    password: str


class InstructorOut(BaseModel):
    user: Instructor
    userType: str

    class Config: 
        orm_mode: True


class UserOut(BaseModel):
    user: User
    userType: str

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
