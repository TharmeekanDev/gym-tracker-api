from fastapi import FastAPI

app = FastAPI(title="Gym Tracker API")  ##creates your application object

@app.get("/")  ##"when someone sends a GET request to /, run the function below
def root():
    return {"message": "Welcome to the Gym Tracker APIs!"}

##Path parameters
# @app.get("/exercises/{exercise_id}")
# def get_exercise(exercise_id:int):
#     return {"exercise_id": exercise_id, "name": "Bench Press", "muscle_group": "Chest"}

##Query parameters
@app.get("/exercises")
def list_exercises(muscle: str | None = None, limit : int = 10):
    return {"muscle_filter" : muscle, "limit": limit}

##For POST and PUT, data arrives in the request body as JSON. You describe its shape with a Pydantic model:

from pydantic import BaseModel
from fastapi import status

class ExerciseCreate(BaseModel):
    name:str
    muscle_group: str
    equipment: str | None = None

@app.post("/exercises",status_code= status.HTTP_201_CREATED)
def create_exercise(exercise: ExerciseCreate):
    return {"message": "Exercise created successfully", "exercise": exercise}
    ##Pydantic rejects invalid data before your function even runs. eg: send post request with {"name": "Squat"} and it will return a 422 error because muscle_group is required.

'''status_code=status.HTTP_201_CREATED tells FastAPI which HTTP status code to send back when this endpoint succeeds.
Without it, FastAPI uses the default for POST, which is 200 OK. That works, but it's less accurate. With it, a successful request returns 201 Created, which is the standard way to say "I made a new resource."'''

from fastapi import HTTPException
@app.get("/exercises/{exercise_id}")
def get_exercise(exercise_id: int):
    if exercise_id !=1:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"exercise_id": 1, "name": "Bench Press", "muscle_group": "Chest"}