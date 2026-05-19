from sqlalchemy import String, Column, Boolean, Integer
from database import Base

class Note(Base):
    __tablename__="notes"

    id=Column(String, primary_key=True)
    title=Column(String)
    content=Column(String)
    category=Column(String)
    author=Column(String)
    completed=Column(Boolean)


class Users(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True , index=True)
    username=Column(String)
    email=Column(String, unique=True)
    password=Column(String)

