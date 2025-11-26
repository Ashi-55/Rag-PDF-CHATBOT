import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.core.config import settings

class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.vector_store = self._load_or_create_index()

    def _load_or_create_index(self):
        if os.path.exists(settings.FAISS_INDEX_PATH):
            try:
                return FAISS.load_local(
                    settings.FAISS_INDEX_PATH, 
                    self.embeddings,
                    allow_dangerous_deserialization=True # Local file, safe to assume trusted
                )
            except Exception as e:
                print(f"Error loading index: {e}. Creating new one.")
                return None
        return None

    def add_documents(self, documents: List[Document]):
        if not documents:
            return
            
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
        
        self.vector_store.save_local(settings.FAISS_INDEX_PATH)

    def as_retriever(self):
        if self.vector_store is None:
            # Return an empty retriever or handle gracefully if no index exists
            # For now, we'll create a dummy empty index to avoid crashing
            empty_store = FAISS.from_texts([""], self.embeddings)
            return empty_store.as_retriever()
        return self.vector_store.as_retriever()
