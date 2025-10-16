from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class FileType(str, Enum):
    IMAGE = "image"
    PDF = "pdf"

class OCRModel(str, Enum):
    RECEIPT = "prebuilt-receipt"
    INVOICE = "prebuilt-invoice"
    LAYOUT = "prebuilt-layout"
    BUSINESS_CARD = "prebuilt-businessCard"
    ID_DOCUMENT = "prebuilt-idDocument"
    READ = "prebuilt-read"

class AnalysisRequest(BaseModel):
    file_data: str = Field(..., description="Arquivo em base64")
    file_type: FileType = Field(..., description="Tipo do arquivo")
    model: OCRModel = Field(..., description="Modelo OCR a usar")
    options: Optional[Dict[str, Any]] = Field(default={}, description="Opções adicionais")

class AnalysisResponse(BaseModel):
    success: bool
    document_type: Optional[str] = None
    confidence: Optional[float] = None
    extracted_data: Optional[Dict[str, Any]] = None
    raw_response: Optional[Dict[str, Any]] = None
    processing_time: float
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

class ModelsResponse(BaseModel):
    available_models: List[str]