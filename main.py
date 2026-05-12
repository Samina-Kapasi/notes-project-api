from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse

app= FastAPI()

class Notes(BaseModel):
    id:Annotated[str, Field(..., description="Note ID", examples=['N001'])]
    title:Annotated[str, Field(..., min_length=3, max_length=100,description="Title of note")]
    content:Annotated[str, Field(..., description="Content of note")]
    category:Annotated[str, Field(..., description="Category of note")]
    author:Annotated[str, Field(..., description="Author of the note")]
    completed:Annotated[bool, Field( default=False,description="Completion status of notes")]

def load_data():
    with open('notes.json', 'r') as f:
        data= json.load(f)
    return data

def save_data(data):
    with open('notes.json', 'w') as f:
        data=json.dump(data, f)


@app.get("/")
def home():
    return {"message":"Home URL"}


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

@app.post("/create")
def create(notes:Notes):
    data=load_data()

    if notes.id in data:
        raise HTTPException(status_code=401, detail="Note already existed")
    
    data[notes.id]=notes.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201, content="Note addedd successfully")

