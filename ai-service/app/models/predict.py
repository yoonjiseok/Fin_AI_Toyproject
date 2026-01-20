from pydantic import BaseModel

class PredictRequest(BaseModel):
    query: str

class PredictResponse(BaseModel):
    answer: str