# fastapi_tutorial

***

# Pydantic: A Comprehensive Guide to Data Validation in Python

## Executive Summary
Pydantic is a powerful Python library for data validation and settings management using Python type annotations. While Python is dynamically typed, which increases flexibility, that same flexibility can cause runtime errors in production systems. Pydantic enforces type hints at runtime and provides a robust framework for complex validation, reducing repetitive manual checks and boilerplate code.

Pydantic follows a three-step workflow: define a model (schema), instantiate the model with raw data (triggering validation and optional type coercion), and use the validated object. Key features include custom data types (e.g., emails, URLs), field-level and model-level validators, computed fields, nested models, and high performance in Pydantic V2 thanks to a Rust core.

***

## 1. The Core Problem: Dynamic Typing and Validation Scaling

In standard Python, variables can change type at runtime (e.g., an integer becomes a string), which is convenient but risky in production. Incorrectly formatted data can propagate into databases or APIs and cause subtle bugs.

### 1.1 Type Hinting vs. Type Enforcement
- Type hints (e.g., `age: int`) are informative only; Python won’t prevent passing a string where an integer is expected.
- Without Pydantic, developers rely on manual checks:
  - Example: `if type(age) != int: raise TypeError`
- Manual checks are error-prone and verbose.

### 1.2 The Scalability Issue
Manual validation becomes unmanageable because:
- Redundancy: validation code repeats across functions (e.g., `insert_data`, `update_data`).
- Maintenance: adding a new field forces updates in multiple places.
- Complexity: format checks (emails, ranges) require complex regex and boilerplate.

***

## 2. The Pydantic Workflow

Pydantic streamlines validation with a clear three-step process based around `BaseModel`.

1. Build a Model  
   Define a class inheriting from `BaseModel` and declare fields with type hints and constraints.

2. Instantiate  
   Create an object by passing raw data (e.g., a `dict`). Pydantic validates types and values automatically.

3. Utilize  
   Use the validated object in your code. If data is invalid, Pydantic raises `ValidationError` before object creation.

***

## 3. Data Schema Definition

Pydantic models let you precisely control structure, from simple primitives to nested complex containers.

### 3.1 Field Requirements and Defaults
- Required fields: fields declared without a default are mandatory.
- Optional fields: use `Optional[...]` and provide a default (commonly `None`).
- Default values: e.g., `married: bool = False`. If absent in input, defaults are used.

### 3.2 Type Coercion
- Pydantic performs smart coercion. Example: `age: int` with input `"30"` becomes integer `30` automatically.

### 3.3 Complex and Custom Types
- Containers: `List[str]`, `Dict[str, str]` enforce types for elements.
- Specialized types: `EmailStr`, `AnyUrl` validate common formats.

***

## 4. Advanced Validation Techniques

Pydantic supports richer validation and metadata attachment for business logic and documentation.

### 4.1 The `Field` Function and `Annotated`
Use `Field` (often with `Annotated`) to add constraints and metadata:
- Numeric constraints: `gt`, `lt`, `ge`, `le`.
- String constraints: `max_length`, `min_length`.
- Metadata: `title`, `description`, `examples` (useful for auto API docs like FastAPI).
- Strict mode: `Field(..., strict=True)` disables coercion and enforces exact types.

### 4.2 Field Validators
- Use `@field_validator` to apply custom logic to single fields.
- Use cases:
  - Domain checks (e.g., ensure email domain is `hdfc.com`).
  - Transformations (e.g., uppercase a string).
- Modes:
  - `before`: validate raw input prior to built-in coercion.
  - `after` (default): validate after coercion into the target type.

### 4.3 Model Validators
- Use `@model_validator` when validation relies on multiple fields.
- Example: “If `age > 60`, `emergency_contact` must be provided.” This requires model-wide access.

***

## 5. Architectural Features

### 5.1 Computed Fields
- Computed fields are derived at runtime from other fields.
- Example: calculate `bmi` from `height` and `weight` using `@computed_field` and `@property`.

### 5.2 Nested Models
- Models can embed other models for hierarchical structures (e.g., an `Address` model inside a `Patient` model).
- Benefits:
  - Reusability
  - Readability
  - Automatic validation of nested data

***

## 6. Data Exportation

Pydantic models can be converted back to common formats:
- `model_dump()` — returns a Python `dict`.
- `model_dump_json()` — returns a JSON string.

### 6.1 Export Controls
- `include`: export only specified fields.
- `exclude`: omit listed fields.
- `exclude_unset`: export only fields explicitly provided during creation (omitting defaults).

***

## 7. Performance and Compatibility

- Pydantic V2 uses a Rust core for its validation engine, yielding significant speed improvements.
- It’s a common foundation for modern Python libraries (e.g., FastAPI) and is widely used in data science for ML pipelines and configuration management (including YAML).

***

## 8. Conclusion

Pydantic converts Python’s flexible typing into a structured, production-ready environment. Centralizing validation in models removes boilerplate, ensures data integrity, and creates self-documenting schemas. Whether validating API inputs or cleaning ML pipeline data, Pydantic is an essential tool for robust, maintainable codebases.

***

# 🩺 Patient Data Model with Pydantic

This notebook demonstrates how to use **Pydantic** for data validation and type enforcement in Python.  
Every field in a Pydantic model is **required by default**. To make a field optional, use `Optional` from the `typing` module and set its default value to `None`.

---

## 📌 Key Features in the Model
- **Validation with `Field`**: Enforce constraints such as `min_length`, `max_length`, `gt` (greater than), and descriptive metadata.
- **Annotated Types**: Use `Annotated` to combine type hints with validation rules.
- **Automatic Type Conversion**: Pydantic can convert compatible types (e.g., `'30'` → `30`).
- **Optional Fields**: Mark fields optional with `Optional[...] = None`.

---

## 🧑‍⚕️ Patient Model Fields
- `name`: String, 2–50 characters, with examples.
- `email`: Valid email address (`EmailStr`).
- `Linkdln_profile`: Valid URL (`AnyUrl`).
- `age`: Integer.
- `weight`: Float, must be greater than zero.
- `married`: Boolean, optional with description.
- `allergies`: List of strings (e.g., `["pollen", "dust"]`).
- `contact_details`: Dictionary of key-value pairs (e.g., `{"email": "...", "phone": "..."}`).

---

## ⚙️ Functions
- **`insert_patient_data(patient: Patient)`**  
  Prints patient details and simulates inserting into a database.

- **`update_patient_data(patient: Patient)`**  
  Prints patient details and simulates updating in a database.

---

## 🧪 Example Usage
```python
patient_info = {
    "name": "nitish",
    "age": 30,
    "email": "nitish@gmail.com",
    "Linkdln_profile": "https://www.linkedin.com/in/nitish",
    "weight": 91,
    "married": False,
    "allergies": ["pollen", "dust"],
    "contact_details": {"email": "abc@gmail.com", "phone": "1234567890"}
}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)


# 🩺 Patient Data Model with Model Validator

This notebook demonstrates how to use **Pydantic’s `model_validator`** to enforce rules that depend on relationships between multiple fields in a model.  
Unlike `field_validator`, which validates individual fields, `model_validator` runs **after all fields are validated** and allows us to check cross-field logic.

---

## 📌 Scenario
We want to ensure that:
- If a patient’s **age is above 60**, then **emergency contact details must be provided** in `contact_details`.

This is a classic case where **field-level validation is not enough**, and we need **model-level validation**.

---

## 🧑‍⚕️ Patient Model Fields
- `name`: String
- `email`: Valid email (`EmailStr`)
- `age`: Integer
- `weight`: Float
- `married`: Boolean
- `allergies`: List of strings
- `contact_details`: Dictionary of key-value pairs (e.g., `{"phone": "...", "emergency": "..."}`)

---

## ⚙️ Model Validator
```python
@model_validator(mode='after')
def validate_emergency_contact(cls, model):
    if model.age > 60 and 'emergency' not in model.contact_details:
        raise ValueError('Emergency contact details are required for patients above 60 years of age')
    return model

# 🩺 Patient Data Model with Computed Field (BMI)

This notebook demonstrates how to use **Pydantic’s `computed_field` decorator** to add derived attributes to a model.  
Computed fields are **not stored directly in the input data** but are calculated dynamically based on other fields.

---

## 📌 Scenario
We want to automatically calculate a patient’s **Body Mass Index (BMI)** using their `weight` and `height` fields.  
Instead of manually computing BMI every time, we define it as a **computed property** inside the model.

---

## 🧑‍⚕️ Patient Model Fields
- `name`: String
- `email`: Valid email (`EmailStr`)
- `age`: Integer
- `weight`: Float (kg)
- `height`: Float (cm)
- `married`: Boolean
- `allergies`: List of strings
- `contact_details`: Dictionary of key-value pairs (e.g., `{"emergency": "...", "phone": "..."}`)

---

## ⚙️ Computed Field
```python
@computed_field
@property
def calculate_bmi(self) -> float:
    bmi = round(self.weight / (self.height / 100 ** 2), 2)
    return bmi


Here’s a polished **Markdown (`%md`) documentation cell** for your nested Pydantic model example, highlighting the benefits of **nested models** and the use of `model_dump` options:

```markdown
# 🩺 Patient Data Model with Nested Models

This notebook demonstrates how to use **nested Pydantic models** to improve **reusability, readability, and validation**.  
By defining separate models (e.g., `Address`), we can embed them inside other models (e.g., `Patient`), making our code more organized and maintainable.

---

## 📌 Benefits of Nested Models
- **Reusability**: Define once, reuse across multiple models.
- **Readability**: Clearer data structure; nested entities are explicit.
- **Validation**: Each nested model is validated independently, making debugging easier.

---

## 🧑‍⚕️ Address Model
```python
class Address(BaseModel):
    city: str
    state: str
    country: str
    pincode: str
```

## 🧑‍⚕️ Patient Model
```python
class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
```

---

## 🧪 Example Usage
```python
address_dict = {"city": "delhi", "state": "delhi", "country": "india", "pincode": "110001"}
address1 = Address(**address_dict)

patient_info = {"name": "nitish", "gender": "male", "age": 30, "address": address_dict}
patient1 = Patient(**patient_info)

print(patient1)
print(patient1.name)
print(patient1.gender)
print(patient1.age)
print(patient1.address.city)
```

✅ Output shows nested access:
```
name='nitish' gender='male' age=30 address=Address(city='delhi', state='delhi', country='india', pincode='110001')
nitish
male
30
delhi
```

---

## 📤 Exporting Data
Pydantic provides multiple ways to **serialize models**:

- **`model_dump()`** → Python dictionary
- **`model_dump_json()`** → JSON string
- **`exclude` / `include`** → Control which fields are serialized
- **`exclude_unset=True`** → Exclude fields not explicitly set

### Examples
```python
temp = patient1.model_dump()
print(temp)  # dict

temp2 = patient1.model_dump_json()
print(temp2)  # JSON string

temp3 = patient1.model_dump(exclude={"age"})
print(temp3)  # exclude age

temp4 = patient1.model_dump(exclude={"address": {"state"}})
print(temp4)  # exclude nested field
```

---

## 🔑 Key Takeaways
- Nested models make complex data structures **cleaner and modular**.
- Use `model_dump` and `model_dump_json` for serialization.
- Use `include` and `exclude` to control output fields.
- Use `exclude_unset=True` to omit unset optional fields.

---

***

# FAST API POST


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