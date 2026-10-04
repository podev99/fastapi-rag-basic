# app/services/rag_service.py
import os
import warnings
import logging
from typing import List

# Suppress warnings to keep the terminal output clean and professional
warnings.filterwarnings("ignore")
logging.getLogger("google").setLevel(logging.ERROR)
logging.getLogger("absl").setLevel(logging.ERROR)

import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma  # <-- Updated import to fix LangChain warning
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

# --- Self-Healing Model Selection ---
genai.configure(api_key=settings.GOOGLE_API_KEY)

AVAILABLE_EMBED_MODEL = "models/text-embedding-004"
AVAILABLE_TEXT_MODEL = "models/gemini-1.5-flash"

try:
    available_models = list(genai.list_models())
    
    # 1. Select valid embedding model
    embed_models = [m.name for m in available_models if 'embedContent' in m.supported_generation_methods]
    if embed_models:
        AVAILABLE_EMBED_MODEL = "models/text-embedding-004" if "models/text-embedding-004" in embed_models else embed_models[0]
            
    # 2. Select valid text generation model
    text_models = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
    if text_models:
        safe_models = [m for m in text_models if "2.5" not in m]
        if "models/gemini-1.5-flash" in safe_models:
            AVAILABLE_TEXT_MODEL = "models/gemini-1.5-flash"
        else:
            AVAILABLE_TEXT_MODEL = safe_models[0] if safe_models else text_models[0]
            
except Exception:
    pass

# --- Initialize Core Services ---

# 1. Initialize Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model=AVAILABLE_EMBED_MODEL,
    google_api_key=settings.GOOGLE_API_KEY
)

# 2. Initialize In-Memory Vector Store
vectorstore = Chroma(embedding_function=embeddings)

# 3. Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=AVAILABLE_TEXT_MODEL,
    temperature=0.3,
    google_api_key=settings.GOOGLE_API_KEY
)

def process_and_store_document(file_path: str) -> int:
    """Loads a PDF document and adds its embeddings to the vector store."""
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    chunks = text_splitter.split_documents(documents)
    
    if chunks:
        vectorstore.add_documents(chunks)
        
    return len(chunks)

def format_docs(docs) -> str:
    """Formats retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def ask_question(query: str) -> str:
    """Retrieves context and asks the LLM."""
    try:
        if vectorstore._collection.count() == 0:
            return "I don't have any context yet. Please upload a document first."
    except Exception:
        pass 

    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.RETRIEVER_K})
    
    system_prompt = (
        "You are a helpful AI assistant. Use the following pieces of retrieved context "
        "to answer the question accurately. If you don't know the answer based on the context, "
        "just say that you don't know. Keep the answer concise.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    try:
        return rag_chain.invoke(query)
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"