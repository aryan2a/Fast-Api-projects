# Import the FastAPI class from the fastapi package
from fastapi import FastAPI

# Create an instance (object) of the FastAPI class
# This 'app' object is the main application
app = FastAPI()

# This is a decorator.
# It tells FastAPI:
# "Whenever someone sends a GET request to the '/' (root URL),
# run the function written below."
@app.get("/")

# This is a normal Python function
# It will run when someone visits http://127.0.0.1:8000/
def home():

    # This is the response returned to the client (browser or API caller)
    # It should be a dictionary (key:value pair)
    return {"message": "nothing to fetch"}