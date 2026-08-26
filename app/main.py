from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.documents.router import router as documents_router
from app.rag.router import router as rag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    yield


app = FastAPI(title="Document Query RAG", version="1.0.0", lifespan=lifespan)

app.include_router(documents_router)
app.include_router(rag_router)


@app.get("/")
def health_check():
    return {"status": "healthy"}
