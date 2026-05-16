from fastapi import FastAPI, HTTPException, Path, Query
import json
from fastapi.responses import JSONResponse
from schemas import Notes, Updated_notes
from database import engine
from models import Base


app= FastAPI()


Base.metadata.create_all(bind=engine)

def load_data():
    with open('notes.json', 'r') as f:
        data= json.load(f)
    return data

def save_data(data):
    with open('notes.json', 'w') as f:
        data=json.dump(data, f)


@app.get("/")
def home():
    return {"message":"Database connected"}


@app.get("/notes")
def view_notes():
    data=load_data()
    return data

@app.get("/notes/{note_id}")
def notes_id(note_id: str=Path(..., description="Enter note ID", examples=['N001'])):
    data= load_data()

    if note_id not in data:
        raise HTTPException(status_code=401, detail="Note not found")
    
    return data[note_id]

@app.get("/sort_notes")
def sort_notes(order:str = Query(description="[asc, desc]")):
    data= load_data()

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid choose")
    
    if order=='desc':
        sort_order=True
    else:
        sort_order=False
    
    sorted_data=sorted(data.items(), key=lambda x: x[0], reverse=sort_order)

    return dict(sorted_data)

@app.post("/notes")
def create(notes:Notes):
    data=load_data()

    if notes.id in data:
        raise HTTPException(status_code=409, detail="Note already existed")
    
    data[notes.id]=notes.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"Note added successfully"})

@app.delete("/delete/{note_id}")
def delete(note_id:str= Path(..., description="Note ID", examples=["N001"])):
    data=load_data()

    if note_id not in data:
        raise HTTPException(status_code=404, detail="Note ID not found")
    
    del data[note_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Note ID deleted successfully"})


@app.put("/notes/{note_id}")
def update(note_id:str, update_note:Updated_notes):
    data=load_data()

    if note_id not in data:
        raise HTTPException(status_code=404, detail="Note not found")
    
    data[note_id]=update_note.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=200, content={"message":"Updated successfully"})


@app.get("/search")
def search(title:str= Query(..., description="Title of note")):
    data= load_data()

    result={}

    for note_id, note in data.items():
        if title.lower() in note.get("title","").lower():
            result[note_id]=note

    if not result:
        raise HTTPException(status_code=404, detail="Title not found")
    
    return result

@app.get("/filter_category")
def filter(category:str=Query(description="Category name of note")):
    data=load_data()

    result={}

    for note_id, note in data.items():
        if note.get("category","")==category:
            result[note_id]=note
        
    if not result:
        raise HTTPException(status_code=404, detail="Information not found")
    
    return result

@app.get("/filter_completed_notes")
def filter(completed:bool=Query(description="Completion status of note")):
    data=load_data()

    result={}

    for note_id, note in data.items():
        if note.get("completed", "")==completed:
            result[note_id]=note
    
    if not result:
        raise HTTPException(status_code=404, detail="Information not found")
    
    return result
