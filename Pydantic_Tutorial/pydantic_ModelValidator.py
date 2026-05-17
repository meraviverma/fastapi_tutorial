from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List,Dict,Optional,Annotated

#scenerio 1: We want emergency contact details .
# Model Validator is used to validate the entire model after all the fields have been validated. It is used when we want to validate the relationship between different fields in the model. For example, if we want to ensure that if the age of the patient is above 60 then emergency contact details must be provided, we can use model validator for that purpose.

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Emergency contact details are required for patients above 60 years of age')
        return model  
    
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

patient_info={'name':'nitish','age':70,'email':'abc@hdfc.com','weight':70.5,'married':False,'allergies':['pollen','dust'],'contact_details':{'emergency':'42343243','phone':'1234567890'}}

patient1=Patient(**patient_info) #validation -> type conversion -> field validation

update_patient_data(patient1)

#Output:
# patient1=Patient(**patient_info) #validation -> type conversion -> field validation
#   File "D:\FastApi\myenv\lib\site-packages\pydantic\main.py", line 263, in __init__
#     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
# pydantic_core._pydantic_core.ValidationError: 1 validation error for Patient
#   Value error, Emergency contact details are required for patients above 60 years of age [type=value_error, input_value={'name': 'nitish', 'age':... 'phone': '1234567890'}}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.13/v/value_error