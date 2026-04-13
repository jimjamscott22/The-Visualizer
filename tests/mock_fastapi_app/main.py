from fastapi import FastAPI
from services import create_user_service

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users/")
def create_user(name: str):
    user = create_user_service(name)
    return {"user": user}
