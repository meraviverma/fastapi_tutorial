#Type Validation is not in python
#data validation as not available in python, we can use pydantic for that purpose. It is a library that provides data validation and settings management using Python type annotations.

def insert_patient_data(name:str,age:int):
    print(name)
    print(age)
    print('inserted into database')

insert_patient_data(name="John Doe",age='30')