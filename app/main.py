from fastapi import FastAPI

app = FastAPI(title="Gym Tracker API")  ##creates your application object

@app.get("/")  ##"when someone sends a GET request to /, run the function below
def root():
    return {"message": "Welcome to the Gym Tracker APIs!"}