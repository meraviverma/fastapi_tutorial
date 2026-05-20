from typing import Annotated,Literal

from pydantic import Field,BaseModel,computed_field

from fastapi import FastAPI,Path, HTTPException,Query
from fastapi.responses import JSONResponse
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="Unique identifier for the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description="Full name of the patient",examples=['John Doe'])]
    city:Annotated[str,Field(...,description="City of residence",examples=['New York'])]
    age:Annotated[int,Field(...,description="Age of the patient",examples=[30])]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient",examples=['Male'])]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in cm",examples=[175.5])]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in kg",examples=[70.0])]

@computed_field
@property
def calculate_bmi(self)->float:
    """Calculate BMI using height and weight."""
    bmi=round(self.weight/(self.height/100)**2,2)
    return bmi

@computed_field
@property
def verdict(self)->str:
    """Provide health verdict based on BMI."""
    if self.calculate_bmi<18.5:
        return "Underweight"
    elif 18.5<=self.calculate_bmi<25:
        return "Normal weight"
    elif 25<=self.calculate_bmi<30:
        return "Overweight"
    else:
        return "Obese"
def load_data():
    """Load patient data from a JSON file."""
    with open("D:/FASTAPI/patients.json", "r") as file:
        data=json.load(file)
    return data

@app.get("/")
def hello():
    return {"message":"Welcome to the Patient API"}

@app.get('/about')
def about():
    return {"message":"This is a simple Patient API"}

@app.get('/patients')
def get_patients():
    data=load_data()
    return {"patients": data}

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on basis of height, weight or bmi"),order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending") ):
    """Sort patients by the specified field."""
    
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid options are: {', '.join(valid_fields)}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid options are: 'asc' or 'desc'")
    data = load_data()

    sort_order=True if  order == "desc" else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

def save_data(data):
    """Save patient data to a JSON file."""
    with open("D:/FASTAPI/patients.json", "w") as file:
        json.dump(data, file, indent=4) # Save data with indentation for better readability

@app.post('/create')
def create_patient(patient:Patient):
    """Create a new patient record."""
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude=['id'])  # Convert Pydantic model to a dictionary

    #save into json file
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully", "patient_id": patient.id}, status_code=201)