from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    x: float

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InputData):
    return {"prediction": data.x * 2}
