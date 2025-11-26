import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

    async def process_pdf(self, file_path: str) -> List[Document]:
        """
        Loads a PDF and splits it into chunks.
        """
        loader = PyPDFLoader(file_path)
        # PyPDFLoader is synchronous, but in a real app we might want to run this in a thread pool
        # For simplicity in this demo, we run it directly.
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        return chunks
