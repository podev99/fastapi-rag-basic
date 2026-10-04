# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A lightweight RAG starter kit using LangChain and In-Memory ChromaDB.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS so any frontend can call these APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root_endpoint():
    """Root endpoint to verify the server is live."""
    return {
        "message": "Welcome to the FastAPI RAG Basic API.",
        "docs": "Visit /docs to test the API endpoints."
    }