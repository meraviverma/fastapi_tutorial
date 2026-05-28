from typing import Annotated,Literal, Optional

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

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None,gt=0)]
    gender: Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]

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

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """Update an existing patient record."""
    data = load_data()
    
    # Check if the patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    # Update the existing patient data with the new values
    existing_patient = data[patient_id]
    
    update_data = patient_update.model_dump(exclude_unset=True)  # Get only the fields that were provided in the update request
    #exclude_unset=True ensures that only the fields that were actually provided in the update request are included in the update_data dictionary. This way, we won't overwrite existing values with None if they were not included in the update request.
    
    # Update the existing patient data with the new values provided in the update request
    # We iterate through the update_data dictionary and update the corresponding fields in the existing_patient dictionary. This allows us to only update the fields that were provided in the update request, while keeping the other fields unchanged.
    #example: if the update request only includes a new value for the 'city' field, then only the 'city' field in the existing patient data will be updated, while the other fields like 'name', 'age', etc. will remain unchanged.
    #Example: if the existing patient data is {"name": "John Doe", "city": "New York", "age": 30} and the update request includes {"city": "Los Angeles"}, then after the update, the existing patient data will be updated to {"name": "John Doe", "city": "Los Angeles", "age": 30}.
    for key, value in update_data.items():
        existing_patient[key] = value  # Update the existing patient data with new values
    
    #Once we update the weight or height, we need to recalculate the BMI and verdict as they are computed fields based on weight and height. So we need to update those fields as well in the existing patient data.
    # Save the updated data back to the JSON file

    existing_patient['id']= patient_id  # Ensure the ID becomes part of object
    patient_pydantic_object = Patient(**existing_patient)  # Create a Patient instance to recalculate computed fields like BMI and verdict
    existing_patient=patient_pydantic_object.model_dump(exclude=['id'])  # Update existing patient data with recalculated fields, excluding 'id' as it is already set
    
    data[patient_id] = existing_patient  # Update the patient data in the main data dictionary
    
    save_data(data)
    
    return JSONResponse(content={"message": "Patient updated successfully", "patient_id": patient_id}, status_code=200)

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    """Delete a patient record."""
    data = load_data()
    
    # Check if the patient with the given ID exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    # Remove the patient from the data
    del data[patient_id]
    
    # Save the updated data back to the JSON file
    save_data(data)
    
    return JSONResponse(content={"message": "Patient deleted successfully", "patient_id": patient_id}, status_code=200)