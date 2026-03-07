from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    pin: int

class Patient(BaseModel):
    name: str
    age: int
    address: Address
    age : int

address_dict = {'city': '12331', 'pin': 110059 , 'street': '5th Avenue'}


patient_dict =  {'name': 'John Doe', 'age': 30, 'address': address_dict}

patient1 = Patient(**patient_dict)

print(patient1.name)
print(patient1.address.street)

# better organization of related data (e.g., vitals, address, insurance)

# Reusability: Use  Vitals in muliple models (e.g., Patient, MedicalRecord)

# Readability: Easier for developers and API consumers to understand

# Validation: Nested models are validated automatically-no extra work needed


