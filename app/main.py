from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn

from app.config import settings
from app.models import AnalysisRequest, AnalysisResponse, HealthResponse, ModelsResponse
from app.ocr_service import AzureOCRService
from app.utils import decode_base64_file, validate_file_size

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API para análise de documentos usando Azure OCR"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviço OCR
ocr_service = AzureOCRService()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de health check"""
    return HealthResponse(
        status="healthy",
        service="azure-ocr-api",
        version=settings.API_VERSION
    )

@app.get("/models", response_model=ModelsResponse)
async def list_models():
    """Lista modelos disponíveis"""
    return ModelsResponse(
        available_models=[
            "prebuilt-receipt",
            "prebuilt-invoice",
            "prebuilt-layout", 
            "prebuilt-businessCard",
            "prebuilt-idDocument",
            "prebuilt-read"
        ]
    )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(request: AnalysisRequest):
    """
    Analisa documento usando Azure OCR
    """
    try:
        # Validar entrada
        if not request.file_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file_data é obrigatório"
            )
        
        # Decodificar base64
        try:
            file_data, mime_type = decode_base64_file(request.file_data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Validar tamanho do arquivo
        if not validate_file_size(file_data, settings.MAX_FILE_SIZE):
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE} bytes"
            )
        
        logger.info(f"Processando arquivo: {mime_type}, modelo: {request.model}")
        
        # Processar com Azure OCR
        result = await ocr_service.analyze_document(file_data, request.model)
        
        return AnalysisResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )