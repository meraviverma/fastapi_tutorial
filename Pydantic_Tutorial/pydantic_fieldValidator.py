from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

#scenerio 1: We want emergency contact details .

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']

        domain= value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Email domain must be one of the following: {", ".join(valid_domains)}')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
    
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print('inserted into database')

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print('updated in database')

patient_info={'name':'nitish','age':30,'email':'abc@hdfc.com','weight':70.5,'married':False,'allergies':['pollen','dust'],'contact_details':{'email':'def@gmail.com','phone':'1234567890'}}

patient1=Patient(**patient_info) #validation -> type conversion -> field validation

update_patient_data(patient1)

#Output:
#  input_value='abc@gmail.com', input_type=str]
#     For further information visit https://errors.pydantic.dev/2.13/v/value_error
# (myenv) PS D:\FastApi> & d:\FastApi\myenv\Scripts\python.exe d:/FastApi/Pydantic_Tutorial/pydantic_fieldValidator.py
# nitish
# abc@hdfc.com
# 30
# 70.5
# updated in database