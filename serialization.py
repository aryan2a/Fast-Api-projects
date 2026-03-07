from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    pin: int

class Patient(BaseModel):
    name: str
    age: int
    address: Address
    gender:str = "dont want to reveal"

address_dict = {'city': '12331', 'pin': 110059 , 'street': '5th Avenue'}


patient_dict =  {'name': 'John Doe', 'age': 30, 'address': address_dict}

patient1 = Patient(**patient_dict)
'''


temp = patient1.model_dump(exclude={'address':['street']})
# above will give a dict excluding street in address

'''

temp = patient1.model_dump(exclude_unset=True)
# above will not give fields not set in patient_dict


'''temp1 = patient1.model_dump_json
# above will give in json format
although python will receive it as string but if you export you will get a json file
'''


print(temp)

print(type(temp))



