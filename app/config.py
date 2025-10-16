import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Azure OCR
    DI_KEY = os.getenv("DI_KEY")
    DI_ENDPOINT = os.getenv("DI_ENDPOINT")
    
    # API
    API_TITLE = "Azure OCR API"
    API_VERSION = "1.0.0"
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # CORS
    ALLOWED_ORIGINS = ["*"]  # Configure conforme necessário
    
    # Validação
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    SUPPORTED_FORMATS = ["image/jpeg", "image/png", "application/pdf"]

settings = Settings()