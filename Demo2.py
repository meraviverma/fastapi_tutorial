from fastapi import FastAPI,Path, HTTPException,Query
import json

## Require sort by age, and make optional.

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

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to view", example="P001")):
    """View details of a specific patient by ID."""
    #load all the patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")
    #return {"error": "Patient not found"}

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on basis of height, weight or bmi"),order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending") ):
    """Sort patients by age if the query parameter is set to true."""
    
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid options are: {', '.join(valid_fields)}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Valid options are: 'asc' or 'desc'")
    data = load_data()

    sort_order=True if  order == "desc" else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data