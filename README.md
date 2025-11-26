# RAG PDF Chatbot Backend

A production-grade backend for a Retrieval-Augmented Generation (RAG) Chatbot capable of ingesting PDFs and answering questions based on their content.

## Features
- **PDF Ingestion**: Upload and chunk multiple PDF documents.
- **Vector Store**: Uses FAISS for efficient similarity search.
- **RAG Pipeline**: LangChain + OpenAI for context-aware answers.
- **API**: FastAPI with Swagger UI.

## Setup

1.  **Clone the repository** (if applicable).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    - Copy `.env.example` to `.env`.
    - Add your `OPENAI_API_KEY`.
    ```bash
    cp .env.example .env
    # Edit .env
    ```

## Running the Server

```bash
cd rag_chatbot
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Swagger UI documentation: `http://localhost:8000/docs`.

## API Endpoints

### `POST /upload`
Upload a PDF file to be indexed.
- **Body**: `multipart/form-data` with `file` field.

### `POST /ask`
Ask a question about the uploaded documents.
- **Body**: JSON `{"query": "Your question here"}`

## Testing

You can use the provided `test_api.py` script (requires `httpx`):

```bash
pip install httpx
python test_api.py
```
