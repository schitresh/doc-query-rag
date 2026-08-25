from fastapi import FastAPI

from app.routes.document_router import router as document_router

app = FastAPI(title="Document Query RAG", version="1.0.0")

app.include_router(document_router)


@app.get("/")
def health_check():
    return {"status": "healthy"}
