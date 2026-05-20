Here’s a beautifully structured **%md documentation block** you can drop directly into your Jupyter Notebook. It explains each function, class, and endpoint in detail, making your FastAPI project self-explanatory and professional.

```markdown
# 🏥 Patient API Documentation

This API is built using **FastAPI** and **Pydantic** to manage patient records.  
It demonstrates model validation, computed fields, JSON file persistence, and RESTful endpoints.

---

## 📌 Imports and Setup
- **typing.Annotated, Literal** → Used for type hints and restricting values (e.g., gender).
- **pydantic.BaseModel, Field, computed_field** → Define data models with validation and computed properties.
- **fastapi.FastAPI, Path, HTTPException, Query** → Core FastAPI framework for building APIs.
- **fastapi.responses.JSONResponse** → Custom JSON responses with status codes.
- **json** → Read/write patient data from a JSON file.

---

## 🧑‍⚕️ Patient Model

```python
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique identifier", examples=['P001'])]
    name: Annotated[str, Field(..., description="Full name", examples=['John Doe'])]
    city: Annotated[str, Field(..., description="City of residence", examples=['New York'])]
    age: Annotated[int, Field(..., description="Age", examples=[30])]
    gender: Annotated[Literal['male','female','others'], Field(..., description="Gender", examples=['Male'])]
    height: Annotated[float, Field(..., gt=0, description="Height in cm", examples=[175.5])]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg", examples=[70.0])]
```

### ✅ Features
- **Validation**: Ensures correct types (e.g., `int` for age, `float` for height/weight).
- **Constraints**: `gt=0` prevents invalid height/weight values.
- **Examples**: Provide sample values for API docs.

---

## ⚖️ Computed Fields

### 1. **BMI Calculation**
```python
@computed_field
@property
def calculate_bmi(self) -> float:
    bmi = round(self.weight / (self.height/100)**2, 2)
    return bmi
```
- Formula: \( BMI = \frac{weight}{(height/100)^2} \)
- Rounded to **2 decimal places**.
- Automatically computed whenever patient data is accessed.

### 2. **Health Verdict**
```python
@computed_field
@property
def verdict(self) -> str:
    if self.calculate_bmi < 18.5:
        return "Underweight"
    elif 18.5 <= self.calculate_bmi < 25:
        return "Normal weight"
    elif 25 <= self.calculate_bmi < 30:
        return "Overweight"
    else:
        return "Obese"
```
- Uses **BMI ranges** to classify health status:
  - `<18.5` → Underweight  
  - `18.5–24.9` → Normal weight  
  - `25–29.9` → Overweight  
  - `≥30` → Obese  

---

## 📂 Data Handling Functions

### **Load Data**
```python
def load_data():
    with open("D:/FASTAPI/patients.json", "r") as file:
        data = json.load(file)
    return data
```
- Reads patient records from a JSON file.
- Returns a dictionary of patient data.

### **Save Data**
```python
def save_data(data):
    with open("D:/FASTAPI/patients.json", "w") as file:
        json.dump(data, file, indent=4)
```
- Writes patient records back to JSON.
- Uses `indent=4` for readability.

---

## 🌐 API Endpoints

### 1. **Root Endpoint**
```python
@app.get("/")
def hello():
    return {"message": "Welcome to the Patient API"}
```
- Simple welcome message.

---

### 2. **About Endpoint**
```python
@app.get("/about")
def about():
    return {"message": "This is a simple Patient API"}
```
- Provides API description.

---

### 3. **Get Patients**
```python
@app.get("/patients")
def get_patients():
    data = load_data()
    return {"patients": data}
```
- Returns all patient records.

---

### 4. **Sort Patients**
```python
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by height, weight, or bmi"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Valid options: {', '.join(valid_fields)}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'")
    
    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data
```

- **Query Parameters**:
  - `sort_by`: height, weight, or bmi.
  - `order`: asc (default) or desc.
- **Validation**: Raises error for invalid fields/orders.
- **Sorting**: Uses Python’s `sorted()` with `lambda`.

---

### 5. **Create Patient**
```python
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully", "patient_id": patient.id}, status_code=201)
```

- **Input**: Patient object (validated by Pydantic).
- **Checks**: Prevents duplicate IDs.
- **Persistence**: Saves new patient to JSON file.
- **Response**: Returns success message with patient ID.

---

## 🎯 Summary
- **Models**: Patient schema with validation and computed fields.
- **Functions**: Load/save JSON data.
- **Endpoints**: CRUD-like operations (read, sort, create).
- **Error Handling**: Uses `HTTPException` for invalid inputs.

---

✨ With this documentation, your notebook will serve as both **code** and **guidebook**, making it easy for anyone to understand and extend your Patient API.
```

Would you like me to also create a **diagram (Graphviz)** showing the flow between `Patient Model → Functions → Endpoints → JSON File`? That would visually tie everything together.