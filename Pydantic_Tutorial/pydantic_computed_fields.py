from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    height:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/(self.height/100**2),2)
        return bmi

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.calculate_bmi) # we can access computed field like this
    print('updated in database')

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.calculate_bmi) # we can access computed field like this
    print('inserted into database')

patient_info={'name':'nitish','age':30,'height':170,'email':'nitish@example.com','weight':70.5,'married':False,'allergies':['pollen','dust'],'contact_details':{'emergency':'42343243','phone':'1234567890'}}    

patient1=Patient(**patient_info) #validation -> type conversion -> field validation
update_patient_data(patient1)