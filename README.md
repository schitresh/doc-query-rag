# Doc Query RAG

A Retrieval-Augmented Generation (RAG) platform that allows users to organize documents into folders, upload files, and interactively chat with their content using vector search and Google Gemini.

---

## 🚀 Features

- **📁 Folder & Collection Organization**: Group documents by folders to query specific document subsets or contextual workspaces.
- **📄 Multi-Format Ingestion**: Supports `.pdf`, `.md`, and `.txt` documents.
- **✂️ Text Processing & Chunking**: Extracts text and splits documents into overlapping chunks for semantic retrieval.
- **🧠 Vector Embeddings & Similarity Search**: Utilizes Google Gemini embeddings with PostgreSQL and the `pgvector` extension for similarity matching.
- **💬 Contextual RAG Chat**: Answers user questions grounded in document context with source references and relevance scores.
- **🖥️ Streamlit Web Interface**: Dual-pane dashboard featuring folder navigation, document uploads, and an interactive chat interface.
- **⚡ RESTful FastAPI Backend**: Async API with automatic OpenAPI/Swagger documentation.

---

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/), [SQLAlchemy](https://www.sqlalchemy.org/), [Pydantic](https://docs.pydantic.dev/)
- **LLM & Embeddings**: [Google GenAI SDK](https://github.com/google/google-genai) (`gemini-3.1-flash-lite`, `gemini-embedding-001`)
- **Document Parsing**: [PyPDF](https://pypdf.readthedocs.io/)
- **Database & Vector Search**: [PostgreSQL](https://www.postgresql.org/) with [pgvector](https://github.com/pgvector/pgvector)
- **Frontend**: [Streamlit](https://streamlit.io/), [HTTPX](https://www.python-httpx.org/)

## 📋 Prerequisites

- **Python**: `3.10+` (tested with Python 3.11/3.12)
- **PostgreSQL**: Version `14+` with the **`pgvector`** extension installed
- **Google Gemini API Key**: [Get an API key from Google AI Studio](https://aistudio.google.com/)

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd doc-query-rag
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure PostgreSQL & pgvector are running:**
   Make sure your PostgreSQL instance is running and the target database exists:
   ```bash
   createdb doc_query_db
   ```
   _(The backend automatically creates the `vector` extension and required tables on startup)._

---

## 🚦 Running the Application

### 1. Start the Backend Server

Export your environment variables and start the FastAPI server with Uvicorn:

```bash
# Load environment variables
source .envrc

# Start backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 2. Start the Frontend Server

In a new terminal window (with the virtual environment activated and environment variables loaded):

```bash
# Load environment variables
source .envrc

# Start Streamlit application
streamlit run frontend/app.py
```

- **Frontend UI**: `http://localhost:8501`

---

## 🔌 API Reference Overview

| Method | Endpoint            | Description                                         |
| :----- | :------------------ | :-------------------------------------------------- |
| `GET`  | `/health`           | Health check endpoint                               |
| `GET`  | `/folders`          | List all available folders                          |
| `POST` | `/folders`          | Create a new folder                                 |
| `GET`  | `/documents`        | List documents (supports filtering by `folder_id`)  |
| `POST` | `/documents/upload` | Upload & process a document (`.pdf`, `.md`, `.txt`) |
| `POST` | `/rag/query`        | Ask a question and retrieve context-aware answers   |
