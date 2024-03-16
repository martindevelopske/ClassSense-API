from .database import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean, Table, Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, mapped_column, Mapped




class Users(Base):
    __tablename__='users'

    id: Mapped[int] =mapped_column(Integer, primary_key=True, nullable=False )
    email=mapped_column(String, nullable=False, unique=True)
    password=mapped_column(String, nullable=False)
    created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    roles: Mapped['Roles']= relationship(back_populates="users", secondary="user_roles")

class Roles(Base):
    __tablename__="roles"

    id=mapped_column(Integer, primary_key=True, nullable=False )
    role_name=mapped_column(String, nullable=False, unique=True)
    role_description=mapped_column(String)

    users: Mapped["Users"]= relationship(back_populates="roles", secondary="user_roles")

class Instructors(Base):
    __tablename__='instructors'

    id: Mapped[int] =mapped_column(Integer, primary_key=True, nullable=False )
    email=mapped_column(String, nullable=False, unique=True)
    password=mapped_column(String, nullable=False)
    created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    sessions= relationship("Sessions", back_populates="instructors")





class Locations(Base):
    __tablename__="locations"

    id=mapped_column(Integer, primary_key=True, nullable=False )
    location_name=mapped_column(String, nullable=False, unique=True)
    location_description=mapped_column(String)
    capacity= mapped_column(Integer, nullable=True)

    sessions= relationship("Sessions", secondary="session_location")

class SessionLocation(Base):
    __tablename__="session_location"
    id=mapped_column(Integer, primary_key=True)
    session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    location_id= mapped_column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)


# #association table
# user_roles= Table(
#     "user_roles",
#     Base.metadata, 
#     Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
#     Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
#     )
class UserRoles(Base):
    __tablename__="user_roles"

    id=mapped_column(Integer, primary_key=True)
    role_id= mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class Sessions(Base):
    __tablename__="sessions"

    id=mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name= mapped_column(String, nullable=False)
    instructor_id= mapped_column(Integer, ForeignKey("instructors.id"), primary_key=True, nullable=False)
    location_id= mapped_column(Integer, ForeignKey("locations.id"), primary_key=True, nullable=True)
    status=mapped_column(String, nullable=False)
    created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    instructor : Mapped['Instructors']= relationship(back_populates="sessions", single_parent=True)

class UserSessions(Base):
    __tablename__="user_sessions"

    id=mapped_column(Integer, primary_key=True)
    session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)


class SessionInstructors(Base):
    __tablename__="session_instructors"

    id=mapped_column(Integer, primary_key=True)
    session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    instructor_id= mapped_column(Integer, ForeignKey("instructors.id", ondelete="CASCADE"), primary_key=True, nullable=False)

class Attendance(Base):
    __tablename__="attendance"

    id=mapped_column(Integer, primary_key=True)
    user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
