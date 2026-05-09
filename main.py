from fastapi import FastAPI
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



