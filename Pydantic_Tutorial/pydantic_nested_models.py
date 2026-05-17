from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Optional,Annotated

#benefit of nested models is that we can reuse the same model in different places. For example, if we have a model for address and we want to use it in patient model, we can create a separate model for address and then use it in patient model. This way we can avoid code duplication and also make our code more organized and maintainable.

#readability is also improved as we can see the structure of the data more clearly. For example, if we have a nested model for address, we can see that the address is a separate entity and it has its own fields. This makes it easier to understand the data structure and also makes it easier to work with the data.

#valiation is also improved as we can validate the nested model separately. For example, if we have a nested model for address, we can validate the address fields separately and then validate the patient model. This way we can ensure that the data is valid and also make it easier to debug if there are any issues with the data.

class Address(BaseModel):
    city:str
    state:str
    country:str
    pincode:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address

address_dict={'city':'delhi','state':'delhi','country':'india','pincode':'110001'}
address1=Address(**address_dict)
    
patient_info={'name':'nitish','gender':'male','age':30,'address':address_dict}

patient1=Patient(**patient_info)
print(patient1)
print(patient1.name)
print(patient1.gender)
print(patient1.age)
print(patient1.address.city)    
print(patient1.address.state)
print(patient1.address.country)
print(patient1.address.pincode)