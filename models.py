from sqlalchemy import String, Column, Boolean
from database import Base

class Note(Base):
    __tablename__="notes"

    id=Column(String, primary_key=True)
    title=Column(String)
    content=Column(String)
    category=Column(String)
    author=Column(String)
    completed=Column(Boolean)

