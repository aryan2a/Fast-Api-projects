from pydantic import BaseModel , EmailStr , AnyUrl , Field ,field_validator , model_validator
from typing import List, Optional, Dict
from typing_extensions import Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(min_length=2 , max_length=50 , description="full name of the patient")]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int
    weight: Annotated[float, Field(default = None , gt = 0 , strict = True , description="weight of the patient in kgs")]
    married: Annotated[bool, Field(description="marital status of the patient")]
    allergies: Optional[List[str]] = None
    contact_details: Dict[str,str]

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls , value):
        valid_domains = ['hdfc.com','icic.com','pnb.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Email domain is not allowed')
        return value
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients above 60 years')
        return model
    


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('updated')
 



patient_info = {'name': 'nitish' , 'age': 65 , 'weight': 44, 'married': True,'contact_details': {'phone': '1234567890'}, 'email': 'abc@hdfc.com' , 'linkedin_url':'https://www.linkedin.com/in/abc/'}

'''
patient_info = {'name': 'nitish' , 'age': 'thirty'}
the above code will raise validation error because age is expected to be int

patient_info = {'name': 'nitish' , 'age': '24'}
the above code will work because pydantic will convert '24' to int
'''

patient1 = Patient(**patient_info)
# ** is used to unpack the dictionary

insert_patient_data(patient1)

