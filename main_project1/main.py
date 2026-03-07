from typing_extensions import Annotated, Literal
from typing import Optional
from datetime import date

from fastapi import FastAPI, HTTPException, Query
import json
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field, computed_field

app = FastAPI()
class Patient(BaseModel):
    
    Name: Annotated[str,Field(..., description="Full name of the patient")]
    Age: Annotated[int,Field(..., gt=0 , description="Age of the patient in years")]
    Gender: Annotated[Literal['male','female','other'], Field(..., description="Gender of the patient")]
    Blood_Type: Annotated[Literal['A+','A-','B+','B-','AB+','AB-','O+','O-'], Field(..., description="Blood type of the patient")]
    Medical_Condition: Annotated[str,Field(..., description="Medical condition of the patient")]
    Date_of_Admission: Annotated[str,Field(..., description="Date of admission in YYYY-MM-DD format")]
    Doctor: Annotated[str,Field(..., description="Name of the attending doctor")]   
    Hospital: Annotated[str,Field(..., description="Name of the hospital")]
    Insurance_Provider: Annotated[str,Field(..., description="Name of the insurance provider")]
    Billing_Amount: Annotated[float,Field(..., gt=0 , description="Total billing amount in USD")]
    Room_Number: Annotated[int,Field(..., gt=0 , description="Room number assigned to the patient")]
    Admission_Type: Annotated[Literal['emergency','elective','urgent'], Field(..., description="Type of admission")]
    Discharge_Date: Annotated[str,Field(..., description="Date of discharge in YYYY-MM-DD format")]
    Medication: Annotated[str,Field(..., description="Medications prescribed to the patient")]
    Test_Results: Annotated[Literal['Normal','Abnormal','inconclusive'], Field(..., description="Results of medical tests")]
    
    @computed_field
    @property
    def stay_duration(self) -> int:
        from datetime import datetime
        admission_date = datetime.strptime(self.Date_of_Admission, "%Y-%m-%d")
        discharge_date = datetime.strptime(self.Discharge_Date, "%Y-%m-%d")
        return (discharge_date - admission_date).days

class Patientupdate(BaseModel):
    

    Age: Optional[int] = Field(None, gt=0, description="Age of the patient in years")
    Gender: Optional[Literal['male','female','other']] = Field(None, description="Gender of the patient")
    Blood_Type: Optional[Literal['A+','A-','B+','B-','AB+','AB-','O+','O-']] = Field(None, description="Blood type of the patient")
    Medical_Condition: Optional[str] = Field(None, description="Medical condition of the patient")
    Date_of_Admission: Optional[date] = Field(None, description="Date of admission in YYYY-MM-DD format")
    Doctor: Optional[str] = Field(None, description="Name of the attending doctor")
    Hospital: Optional[str] = Field(None, description="Name of the hospital")
    Insurance_Provider: Optional[str] = Field(None, description="Name of the insurance provider")
    Billing_Amount: Optional[float] = Field(None, gt=0, description="Total billing amount in USD")
    Room_Number: Optional[int] = Field(None, gt=0, description="Room number assigned to the patient")
    Admission_Type: Optional[Literal['emergency','elective','urgent']] = Field(None, description="Type of admission")
    Discharge_Date: Optional[date] = Field(None, description="Date of discharge in YYYY-MM-DD format")
    Medication: Optional[str] = Field(None, description="Medications prescribed to the patient")
    Test_Results: Optional[Literal['Normal','Abnormal','inconclusive']] = Field(None, description="Results of medical tests")

# we did not write name because that we will be using as our path parameter and these fields as our request body 

def load_data():
    with open('healthcare_dataset.json', 'r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('healthcare_dataset.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {"message": "Welcome to the Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient records."}


@app.get("/patient/{name}")
def view_patient(name: str):
    data = load_data()

    for patient in data:
        if patient["Name"].lower() == name.lower():
            return patient

    raise HTTPException(status_code=404, detail="patient not found")

@app.get('/sort')

def sort_patients(sort_by: str = Query(..., description = "sort on the basis of age"), order : str = Query('asc', description = "sort in ascending or descending order")):
    data = load_data()

    if sort_by not in 'Age':
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order parameter")
    
    reverse = True if order == 'desc' else False

    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=reverse)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #load existing data
    data = load_data()

    #check if the patient already exists
    for existing_patient in data:
        if existing_patient["Name"].lower() == patient.Name.lower():
            raise HTTPException(status_code=400, detail="Patient already exists")
    '''
     if my data has id as key then we could have written if patient .id in data: raise HTTPException(status_code=400, detail="Patient already exists")

     data[patient.id] = patient.model_dump() this way we could have added new patient

     Yes, that statement is correct — but ONLY if your data structure is a dictionary keyed by id.

    
 '''
    # if my data has id as key then we could have written if patient .id in data: raise HTTPException(status_code=400, detail="Patient already exists")
    #add new patient
    data.append(patient.model_dump())

    #save updated data  
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201) 

'''
for update we would be making a new pydantic model because in the existing pydantic model we have fields that are necessary but what if 
we dont want to update that field so in that case we will make a new pydantic model where all the fields will be optional 

'''
# ---------------- UPDATE ----------------
@app.patch("/update/{name}")
def update_patient(name: str, update: Patientupdate):
    data = load_data()

    for patient in data:
        if patient["Name"].lower() == name.lower():
            updates = update.model_dump(exclude_unset=True)

            # convert date → string only when present
            if "Date_of_Admission" in updates:
                updates["Date_of_Admission"] = str(updates["Date_of_Admission"])

            if "Discharge_Date" in updates:
                updates["Discharge_Date"] = str(updates["Discharge_Date"])

            patient.update(updates)
            save_data(data)

            return {
                "message": "Patient updated successfully",
                "updated_patient": patient
            }

    raise HTTPException(404, "Patient not found")

@app.delete('/delete/{name}')
def delete_patient(name:str):
    
     data = load_data()

     for patient in data:
        if patient["Name"].lower() == name.lower():
            data.remove(patient)
            save_data(data) 
            return {"message": "Patient deleted successfully"}

     raise HTTPException(status_code=404, detail="patient not found")


     return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)

       
    
