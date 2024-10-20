import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploaded_folder')
    FAISS_INDEX_FOLDER = os.getenv('FAISS_INDEX_FOLDER', 'faiss_index')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    VECTARA_CUSTOMER_ID = os.getenv('VECTARA_CUSTOMER_ID')
    VECTARA_AUTHORIZATION_TOKEN = os.getenv('VECTARA_AUTHORIZATION_TOKEN')
    VECTARA_CORPUS_ID = os.getenv('VECTARA_CORPUS_ID')  # Add this line