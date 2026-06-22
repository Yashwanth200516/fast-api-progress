from fastapi import FastAPI,HTTPException
from models import Students
from database import collection
from routers import auth,student
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.include_router(student.router)
app.include_router(auth.router)


@app.get('/')
def home():
    return {'message':'home page'}

app.mount("/static",StaticFiles(directory="static"),name="static")