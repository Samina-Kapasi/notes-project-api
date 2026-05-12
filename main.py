from fastapi import FastAPI, HTTPException, Path, Query
import json

app= FastAPI()

def load_data():
    with open('notes.json', 'r') as f:
        data= json.load(f)
    return data


@app.get("/")
def home():
    return {"message":"Home URL"}


@app.get("/notes")
def view_notes():
    data=load_data()
    return data

@app.get("/notes/{note_id}")
def notes_id(note_id: str):
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