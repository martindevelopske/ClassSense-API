# from .database import Base
# from sqlalchemy import Integer, String, ForeignKey, Boolean, Table, Column
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from sqlalchemy.sql.expression import text
# from sqlalchemy.orm import relationship, mapped_column, Mapped




# class Users(Base):
#     __tablename__='users'

#     id: Mapped[int] =mapped_column(Integer, primary_key=True, nullable=False )
#     email=mapped_column(String, nullable=False, unique=True)
#     password=mapped_column(String, nullable=False)
#     created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#     roles= relationship("Roles", back_populates="users", secondary="user_roles")

# class Roles(Base):
#     __tablename__="roles"

#     id=mapped_column(Integer, primary_key=True, nullable=False )
#     role_name=mapped_column(String, nullable=False, unique=True)
#     role_description=mapped_column(String)

#     users= relationship("Users", back_populates="roles", secondary="user_roles")

# class Instructors(Base):
#     __tablename__='instructors'

#     id: Mapped[int] =mapped_column(Integer, primary_key=True, nullable=False )
#     email=mapped_column(String, nullable=False, unique=True)
#     password=mapped_column(String, nullable=False)
#     created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#     sessions= relationship("Sessions", back_populates="instructors")





# class Locations(Base):
#     __tablename__="locations"

#     id=mapped_column(Integer, primary_key=True, nullable=False )
#     location_name=mapped_column(String, nullable=False, unique=True)
#     location_description=mapped_column(String)
#     capacity= mapped_column(Integer, nullable=True)

#     sessions= relationship("Sessions", secondary="session_location")

# class SessionLocation(Base):
#     __tablename__="session_location"
#     id=mapped_column(Integer, primary_key=True)
#     session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
#     location_id= mapped_column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)


# # #association table
# # user_roles= Table(
# #     "user_roles",
# #     Base.metadata, 
# #     Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
# #     Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
# #     )
# class UserRoles(Base):
#     __tablename__="user_roles"

#     id=mapped_column(Integer, primary_key=True)
#     role_id= mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
#     user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

# class Sessions(Base):
#     __tablename__="sessions"

#     id=mapped_column(Integer, primary_key=True, nullable=False, unique=True)
#     name= mapped_column(String, nullable=False)
#     instructor_id= mapped_column(Integer, ForeignKey("instructors.id"), primary_key=True, nullable=False)
#     location_id= mapped_column(Integer, ForeignKey("locations.id"), primary_key=True, nullable=True)
#     status=mapped_column(String, nullable=False)
#     created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#     instructor = relationship("Instructors", back_populates="sessions", single_parent=True)

# class UserSessions(Base):
#     __tablename__="user_sessions"

#     id=mapped_column(Integer, primary_key=True)
#     session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
#     user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)


# class SessionInstructors(Base):
#     __tablename__="session_instructors"

#     id=mapped_column(Integer, primary_key=True)
#     session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
#     instructor_id= mapped_column(Integer, ForeignKey("instructors.id", ondelete="CASCADE"), primary_key=True, nullable=False)

# class Attendance(Base):
#     __tablename__="attendance"

#     id=mapped_column(Integer, primary_key=True)
#     user_id= mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
#     session_id= mapped_column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True, nullable=False)
#     created_at=mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    roles = relationship('Roles', back_populates='users', secondary='user_roles')

class Roles(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String, nullable=False, unique=True)
    role_description = Column(String)

    users = relationship('Users', back_populates='roles', secondary='user_roles')

class Instructors(Base):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    sessions = relationship("Sessions", back_populates="instructor")

class Locations(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, nullable=False)
    location_name = Column(String, nullable=False, unique=True)
    location_description = Column(String)
    capacity = Column(Integer, nullable=True)

    sessions = relationship("Sessions", secondary="session_location")

class SessionLocation(Base):
    __tablename__ = 'session_location'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=False)

class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="CASCADE"))

   

class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    instructor = relationship("Instructors", back_populates="sessions")

class SessionMembers(Base):
    __tablename__= "session_members"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


# class UserSessions(Base):
#     __tablename__ = 'user_sessions'

#     id = Column(Integer, primary_key=True)
#     session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class SessionInstructors(Base):
    __tablename__ = 'session_instructors'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False)

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
