from fastapi import FastAPI, HTTPException,Query, Depends
from schemas import Notes, Updated_notes, Create_user
from database import engine, SessionLocal
from models import Base, Note, Users
from sqlalchemy.orm import Session
from hashing import hash_password

app= FastAPI()


Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message":"Database connected"}


@app.get("/test-db")
def test_db(db:Session= Depends(get_db)):
    return {"message":"Database connection working properly"}

@app.post("/notes-db")
def notes_db(notes:Notes, db:Session=Depends(get_db)):
    
    new_notes=Note(
        id=notes.id,
        title=notes.title,
        content=notes.content,
        category=notes.category,
        author=notes.author,
        completed=notes.completed
    )

    db.add(new_notes)
    db.commit()

    return {"message":"Record added successfully"}

@app.get("/get_notes")
def get_notes(db:Session=Depends(get_db)):

    notes=db.query(Note).all()

    return notes

@app.get("/get_note/{note_id}")
def get_note(note_id:str, db:Session=Depends(get_db)):

    note=db.query(Note).filter(Note.id==note_id).first()

    return note

@app.delete("/delete_note/{note_id}")
def delete_note(note_id:str, db:Session=Depends(get_db)):

    note=db.query(Note).filter(Note.id==note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)

    db.commit()

    return {"message":"Note deleted successfully"}

@app.put("/update_note/{note_id}")
def update_note(note_id:str, update_note:Updated_notes, db:Session=Depends(get_db)):
    
    note=db.query(Note).filter(note_id==Note.id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.title= update_note.title
    note.category=update_note.category
    note.content=update_note.content
    note.author=update_note.author
    note.completed=update_note.completed

    db.commit()

    return {"message":"Note updated successfully"}


@app.get("/search")
def search(title:str, db:Session=Depends(get_db)):

    note=db.query(Note).filter(Note.title.contains(title)).all()

    if not note:
        raise HTTPException(status_code=404, detail="Title not found")
    
    return note

@app.get("/filter")
def filter(note_complete:bool, note_category:str, db:Session=Depends(get_db)):

    note=db.query(Note).filter(
        Note.category==note_category,
        Note.completed==note_complete
    ).all()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@app.post("/signup")
def signup(user:Create_user, db:Session=Depends(get_db) ):

    existing_user=db.query(Users).filter(
        Users.email==user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password=hash_password(user.password)

    new_user=Users(
        username= user.username,
        email= user.email,
        password= hashed_password
    )

    db.add(new_user)

    db.commit()

    return {"message":"User Signed Up successfully"}
 