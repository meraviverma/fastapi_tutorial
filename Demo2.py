from fastapi import FastAPI
import json


app = FastAPI()

def load_data():
    """Load patient data from a JSON file."""
    with open("patients.json", "r") as file:
        data=json.load(file)
    return data

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application with about"}

@app.get("/view")
def view():
    data = load_data()
    return data
