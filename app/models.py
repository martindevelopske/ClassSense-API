from .database import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, mapped_column, Mapped




class User(Base):
    __tablename__='users'

    id: Mapped[int] =mapped_column(Integer, primary_key=True, nullable=False )
    email=mapped_column(String, nullable=False, unique=True)
    password=mapped_column(String, nullable=False)
    created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    roles=relationship("Roles", back_populates="user")


class Roles(Base):
    __tablename__="roles"

    id=mapped_column(Integer, primary_key=True, nullable=False )
    role_name=mapped_column(String, nullable=False, unique=True)
    role_description=mapped_column(String)



class Locations(Base):
    __tablename__="locations"

    id=mapped_column(Integer, primary_key=True, nullable=False )
    location_name=mapped_column(String, nullable=False, unique=True)
    location_description=mapped_column(String)


class UserRoles(Base):
    __tablename__="user_roles"

    id=mapped_column(Integer, primary_key=True)
    role_id= mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    user_id= mapped_column(Integer, ForeignKey("users.id"), nullable=False)

class Sessions(Base):
    __tablename__="sessions"

    id=mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name= mapped_column(String, nullable=False)
    instructor_id= mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    location_id= mapped_column(Integer, ForeignKey("locations.id"), primary_key=True, nullable=False)
    status=mapped_column(String, nullable=False)

class UserSessions(Base):
    __tablename__="user_sessions"

    session_id= mapped_column(Integer, ForeignKey("sessions.id"), primary_key=True, nullable=False)
    user_id= mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)


class SessionInstructors(Base):
    __tablename__="session_instructors"

    session_id= mapped_column(Integer, ForeignKey("sessions.id"), primary_key=True, nullable=False)
    instructor_id= mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)

class Attendance(Base):
    __tablename__="attendance"

    user_id= mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    session_id= mapped_column(Integer, ForeignKey("sessions.id"), primary_key=True, nullable=False)
