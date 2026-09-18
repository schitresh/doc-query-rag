# Doc Query RAG

A Retrieval-Augmented Generation (RAG) platform that allows users to organize documents into folders, upload files, and interactively chat with their content using vector search and Google Gemini.

<img width="1282" height="657" alt="image" src="https://github.com/user-attachments/assets/905f6dfe-2ce9-49f0-9ba8-f27917ca74e7" />

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

---

## 🐳 Quick Start with Docker

The easiest way to run the full stack (FastAPI backend, Streamlit frontend, and PostgreSQL with pgvector) without local environment setup:

1. **Configure environment variables:**
   - Open [env/.env.development.main](file:///Users/User/Dashboard/workspace/doc-query-rag/env/.env.development.main) and set your `GEMINI_API_KEY`:
     ```bash
     GEMINI_API_KEY="your_gemini_api_key_here"
     ```

2. **Start the containers:**

   ```bash
   docker compose up --build
   ```

3. **Access the services:**
   - **Frontend UI (Streamlit)**: [http://localhost:8501](http://localhost:8501)
   - **Backend API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Backend Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

4. **Stop the containers:**
   ```bash
   docker compose down
   ```

---

## 💻 Development

Follow these steps to set up and run the project locally for development:

### 1. Prerequisites

- **Python**: `3.10+`
- **PostgreSQL**: Version `14+` with the **`pgvector`** extension installed
- **Google Gemini API Key**: [Get an API key from Google AI Studio](https://aistudio.google.com/)

### 2. Setup Environment & Dependencies

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd doc-query-rag
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv-doc-query-rag
   source .venv-doc-query-rag/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configure Environment Variables

Open [env/.env.development.main](file:///Users/User/Dashboard/workspace/doc-query-rag/env/.env.development.main) and add your `GEMINI_API_KEY`:

```bash
GEMINI_API_KEY="your_gemini_api_key_here"
```

### 4. Database Setup

Ensure PostgreSQL is running and initialize the application database:

```bash
createdb doc_query_db
```

_(The backend automatically creates the `vector` extension and required tables on startup)._

### 5. Running the Application

#### A. Start the Backend Server

Load your environment variables and start the FastAPI server with Uvicorn:

```bash
# Load environment variables & activate venv
source .envrc

# Start backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **API Base URL**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

#### B. Start the Frontend Server

In a new terminal window:

```bash
# Load environment variables & activate venv
source .envrc

# Start Streamlit application
streamlit run frontend/app.py
```

- **Frontend UI**: [http://localhost:8501](http://localhost:8501)

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
