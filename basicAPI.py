from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/users")

def get_users():
    return ["Aryan","Rahul","Ankit","John","Doe"]

            