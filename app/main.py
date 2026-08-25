from fastapi import FastAPI

from app.routes import document_router

app = FastAPI(title="Document Query RAG", version="1.0.0")

app.include_router(document_router)


@app.get("/")
def health_check():
    return {"status": "healthy"}
