from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    married:bool
    allergies:List[str]
    contact_details:Dict[str,str]

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=