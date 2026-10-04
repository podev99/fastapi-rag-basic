# app/api/routes.py
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.api_models import HealthResponse, UploadResponse, ChatRequest, ChatResponse
from app.services.rag_service import process_and_store_document, ask_question

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API is running successfully."""
    return HealthResponse(status="ok", message="System is running smoothly.")

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document (PDF), process it using LangChain, 
    and store embeddings into the in-memory ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Currently, only PDF files are supported.")
    
    temp_file_path = f"temp_{file.filename}"
    
    try:
        # Save uploaded file temporarily for PyPDFLoader to read
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # Process and chunk the document using our RAG service
        chunks_processed = process_and_store_document(temp_file_path)
        
        return UploadResponse(
            filename=file.filename,
            message="Document processed and loaded into memory successfully.",
            chunks_created=chunks_processed
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
        
    finally:
        # Always clean up the temporary file to prevent disk bloat
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    """
    Send a query to the LLM. The system will retrieve relevant context 
    from the uploaded documents in memory to answer the question.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        # Retrieve context and generate answer using LangChain
        answer = ask_question(request.query)
        
        return ChatResponse(
            query=request.query,
            answer=answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")