from pydantic import BaseModel

class Patient(BaseModel):
    name:str
    age:int


#we are passing object
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('inserted into database')

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('updated in database')

# if we pass thirty now the function will fail
# pydantic is smart enoough to convert '30' to 30 and it will work fine
patient_info={'name':'nitish','age':'30'}

patient1=Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)