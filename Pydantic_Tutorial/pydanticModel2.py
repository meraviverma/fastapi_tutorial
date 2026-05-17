from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

#every field in pydantic model is required by default, if we want to make it optional we can use Optional from typing module and set default value to None. For example:

class Patient(BaseModel):
    #name:str
    name:Annotated[str,Field(min_length=2, max_length=50, title="Name of patient", description="Name must be between 2 and 50 characters", example=["John Doe", "Jane Smith"])]  
    email:EmailStr
    Linkdln_profile:AnyUrl
    age:int
    weight:float = Field(gt=0, description="Weight must be greater than zero") # we can also add validation for the fields using Field from pydantic
    #weight:float = Annotated[float,Field(gt=0,strict=True)] # we can also add validation for the fields using Field from pydantic, strict=True will not allow any type conversion and will raise error if the value is not of type float
    #married:bool
    married: Annotated[bool, Field(default=None,description="Is the patient married or not", example=True)]
    allergies:List[str] #allergies: Optional[List[str]] = None # if we want to make it optional need to set default value to None
    #allergies: Optional[List[str]]=Field(max_length=5, description="Maximum of 5 allergies allowed") # we can also add validation for the fields using Field from pydantic
    contact_details:Dict[str,str]


#we are passing object
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.Linkdln_profile)
    print(patient.age)
    print(patient.weight)
    print('inserted into database')

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.Linkdln_profile)
    print(patient.age)
    print(patient.weight)
    print('updated in database')

# if we pass thirty now the function will fail
# pydantic is smart enoough to convert '30' to 30 and it will work fine
patient_info={'name':'nitish','age':30,'email':'nitish@gmail.com','Linkdln_profile':'https://www.linkedin.com/in/nitish','weight':91,'married':False,'allergies':['pollen','dust'],'contact_details':{'email':'abc@gmail.com','phone':'1234567890'}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)