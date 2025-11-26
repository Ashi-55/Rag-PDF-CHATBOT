from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    query: str

class SourceDocument(BaseModel):
    page_content: str
    source: str
    page: int

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]

class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks_processed: int
