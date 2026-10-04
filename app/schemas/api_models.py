# app/schemas/api_models.py
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str

class UploadResponse(BaseModel):
    filename: str
    message: str
    chunks_created: int

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    query: str
    answer: str