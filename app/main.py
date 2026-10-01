from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Gym Tracker API") 

class ExerciseCreate(BaseModel):
    name: str
    muscle_group: str
    equipment: str | None = None

class Exercise(ExerciseCreate):
    id: int

exercises: list[Exercise] = []
next_id = 1

@app.get("/")
def root():
    return {"message": "Welcome to the Gym Tracker APIs!"}

##response_model tells FastAPI the shape of the response, which filters and documents the output., data.model_dump() converts a Pydantic model to a dict.
@app.post("/exercises", response_model=Exercise, status_code=status.HTTP_201_CREATED)
def create_exercise(data: ExerciseCreate):
    global next_id
    exercise = Exercise(id=next_id, **data.model_dump())
    exercises.append(exercise)
    next_id += 1
    return exercise

@app.get("/exercises", response_model=list[Exercise])
def list_exercises(muscle: str | None = None):
    if muscle:
        filtered_exercises = [e for e in exercises if e.muscle_group.lower() == muscle.lower()]
        return filtered_exercises
    return exercises

@app.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id : int):
    for e in exercises:
        if e.id == exercise_id:
            return e
    raise HTTPException(status_code=404, detail="Exercise not found")

