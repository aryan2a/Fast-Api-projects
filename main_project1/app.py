import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Patient Management System", layout="wide")
st.title("🏥 Patient Management System")




# ---------------- SEARCH ----------------
def search_patient():
    name = st.text_input("Enter Patient Name")

    if st.button("Search"):
        res = requests.get(f"{BASE_URL}/patient/{name}")
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Patient not found")


# ---------------- CREATE ----------------
def create_patient():
    st.subheader("Add New Patient")

    patient = {}
    patient["Name"] = st.text_input("Name")
    patient["Age"] = st.number_input("Age", min_value=1)
    patient["Gender"] = st.selectbox("Gender", ["male", "female", "other"])
    patient["Blood_Type"] = st.selectbox(
        "Blood Type",
        ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
    )
    patient["Medical_Condition"] = st.text_input("Medical Condition")
    patient["Date_of_Admission"] = st.text_input("Date of Admission (YYYY-MM-DD)")
    patient["Doctor"] = st.text_input("Doctor")
    patient["Hospital"] = st.text_input("Hospital")
    patient["Insurance_Provider"] = st.text_input("Insurance Provider")
    patient["Billing_Amount"] = st.number_input("Billing Amount", min_value=1.0)
    patient["Room_Number"] = st.number_input("Room Number", min_value=1)
    patient["Admission_Type"] = st.selectbox("Admission Type", ["emergency","elective","urgent"])
    patient["Discharge_Date"] = st.text_input("Discharge Date (YYYY-MM-DD)")
    patient["Medication"] = st.text_input("Medication")
    patient["Test_Results"] = st.selectbox("Test Results", ["Normal","Abnormal","inconclusive"])

    if st.button("Create Patient"):
        res = requests.post(f"{BASE_URL}/create", json=patient)
        if res.status_code == 201:
            st.success("Patient Created Successfully")
        else:
           st.error(res.json()["detail"])



# ---------------- UPDATE ----------------
def update_patient():
    st.subheader("Update Patient")

    name = st.text_input("Enter name to update")

    field = st.selectbox(
        "Select field",
        [
            "Age","Gender","Blood_Type","Medical_Condition",
            "Date_of_Admission","Doctor","Hospital",
            "Insurance_Provider","Billing_Amount","Room_Number",
            "Admission_Type","Discharge_Date","Medication","Test_Results"
        ]
    )

    value = st.text_input("Enter new value")

    if st.button("Update"):
        res = requests.patch(
            f"{BASE_URL}/update/{name}",
            json={field: value}
        )

        if res.status_code == 200:
            st.success("Updated Successfully")
            st.json(res.json())
        else:
            st.error("Update failed")


# ---------------- DELETE ----------------
def delete_patient():
    st.subheader("Delete Patient")

    name = st.text_input("Enter patient name to delete")

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/delete/{name}")
        if res.status_code == 200:
            st.success("Patient Deleted")
        else:
            st.error("Patient not found")


# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Navigation",
    ["Search Patient","Create Patient","Update Patient","Delete Patient"]
)


if   menu == "Search Patient":
    search_patient()
elif menu == "Create Patient":
    create_patient()
elif menu == "Update Patient":
    update_patient()
elif menu == "Delete Patient":
    delete_patient()
