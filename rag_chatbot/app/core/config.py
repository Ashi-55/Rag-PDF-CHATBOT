import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATA_DIR = os.path.join(os.getcwd(), "rag_chatbot", "data")
    FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

settings = Settings()
