from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import settings

app = FastAPI(
    title="RAG PDF Chatbot",
    description="A production-grade RAG backend to chat with your PDFs.",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG PDF Chatbot API. Visit /docs for Swagger UI."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
