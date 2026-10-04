# 🚀 FastAPI RAG Basic Starter Kit

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green)
![Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Flash-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

A lightweight, production-ready **RAG (Retrieval-Augmented Generation)** boilerplate using FastAPI, LangChain, ChromaDB, and Google Gemini. 

Designed for developers who want to clone, run, and understand a fully functional AI system in **under 10 minutes** without dealing with complex database setups or Docker configurations.

## ✨ Key Features

*   **⚡ Zero-Setup Database:** Uses ChromaDB in **In-Memory** mode. No installation or file permissions required. Data lives in RAM and resets when the server stops.
*   **🧠 Modern LangChain (LCEL):** Implements the latest LangChain Expression Language (LCEL) for a clean, readable, and highly efficient RAG pipeline.
*   **🛡️ Self-Healing AI:** Automatically fetches and selects available Google Generative AI models to prevent `404 NOT_FOUND` errors when regional API access changes.
*   **🏗️ Clean Architecture:** Code is beautifully organized into `/api`, `/core`, `/schemas`, and `/services` folders, making it scalable for future upgrades.
*   **🧪 Built-in Unit Tests:** Comes pre-configured with `pytest` and `httpx`, utilizing API mocking for fast, cost-free testing.

## 🛠️ Quick Start Guide

### 1. Prerequisites
*   Python 3.10 or higher.
*   A free Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/)).

### 2. Installation
Clone the repository and set up your virtual environment:

```bash
git clone [https://github.com/your-username/fastapi-rag-basic.git](https://github.com/your-username/fastapi-rag-basic.git)
cd fastapi-rag-basic

# Create and activate virtual environment
py -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create your `.env` file from the provided example:

```bash
cp .env.example .env
```

Open .env and insert your actual Google API Key:

```bash
GOOGLE_API_KEY="your_actual_key_here"
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

Once running, visit http://127.0.0.1:8000/docs to view the interactive Swagger UI.

# 🧪 Standardized Testing Queries

To thoroughly stress-test the RAG capabilities, upload any PDF document via the POST /api/v1/upload endpoint, and then try these standardized queries in the POST /api/v1/chat endpoint:

Overview & Summarization

"Please summarize the main content of this entire document in 3 to 5 concise sentences."

"Based on the document, what is the main purpose of this text, and who is the target audience?"

Detailed Extraction
3. "List all the key numbers, percentages, or dates mentioned in this document."
4. "Identify 3 to 5 of the most important keywords or technical terms defined in the text and briefly explain them."

Reasoning & Synthesis
5. "Based on the provided content, what is the core issue being addressed, and what are the proposed solutions?"
6. "Does this document outline any conclusions or next steps? Please list them clearly."

Output Formatting
7. "Present the key takeaways from this document as a clear bulleted list."
8. "Organize the most critical information from the document into a markdown table with two columns: 'Topic' and 'Details'."

Anti-Hallucination (Crucial Test)
9. "Does this document mention any policies regarding Mars exploration or provide any cooking recipes?"
(The AI must explicitly state that it does not know or the information is not in the document).

# 📂 Project Structure

```text
fastapi-rag-basic/
├── app/
│   ├── api/
│   │   └── routes.py         # FastAPI endpoints (/health, /upload, /chat)
│   ├── core/
│   │   └── config.py         # Environment variables & app settings
│   ├── schemas/
│   │   └── api_models.py     # Pydantic models for request/response validation
│   ├── services/
│   │   └── rag_service.py    # LangChain LCEL pipeline & ChromaDB logic
│   └── main.py               # FastAPI application initialization
├── tests/
│   └── test_api.py           # Unit tests with mocked dependencies
├── .env.example
├── .gitignore
└── requirements.txt
```

# 🚥 Running Tests

To run the automated test suite without consuming your Google API quota:

```bash
pytest -v
```

# 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page. If you found this project helpful, please give it a ⭐️!