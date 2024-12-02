from fastapi import FastAPI
from student import models
from student.database import engine
from student.routers import students

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(students.router)

