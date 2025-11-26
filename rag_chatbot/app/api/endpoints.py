import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import AskRequest, AskResponse, UploadResponse, SourceDocument
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.rag_chain import RAGService
from app.core.config import settings

router = APIRouter()

# Initialize services (Singleton pattern for simplicity in this demo)
doc_processor = DocumentProcessor()
vector_store_service = VectorStoreService()
rag_service = RAGService(vector_store_service)

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Save file locally
    file_path = os.path.join(settings.DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process PDF
        chunks = await doc_processor.process_pdf(file_path)
        
        # Add to Vector Store
        vector_store_service.add_documents(chunks)
        
        return UploadResponse(
            filename=file.filename,
            status="Successfully processed and indexed",
            chunks_processed=len(chunks)
        )
    except Exception as e:
        # Clean up file if processing fails
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    try:
        result = rag_service.get_answer(request.query)
        
        answer = result["answer"]
        source_docs = []
        for doc in result.get("context", []):
            source_docs.append(SourceDocument(
                page_content=doc.page_content,
                source=os.path.basename(doc.metadata.get("source", "unknown")),
                page=doc.metadata.get("page", 0)
            ))
            
        return AskResponse(answer=answer, sources=source_docs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
