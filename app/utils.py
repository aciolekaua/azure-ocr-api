import base64
import io
from typing import Tuple
import mimetypes

def decode_base64_file(base64_string: str) -> Tuple[bytes, str]:
    """
    Decodifica string base64 e retorna dados e tipo MIME
    """
    try:
        # Remove prefixo data: se existir
        if base64_string.startswith('data:'):
            header, data = base64_string.split(',', 1)
            mime_type = header.split(':')[1].split(';')[0]
        else:
            data = base64_string
            mime_type = None
        
        # Decodifica base64
        file_data = base64.b64decode(data)
        
        # Detecta tipo MIME se não fornecido
        if not mime_type:
            mime_type, _ = mimetypes.guess_type('file')
            if not mime_type:
                mime_type = 'application/octet-stream'
        
        return file_data, mime_type
        
    except Exception as e:
        raise ValueError(f"Erro ao decodificar base64: {str(e)}")

def create_file_object(file_data: bytes) -> io.BytesIO:
    """
    Cria objeto file-like a partir de bytes
    """
    return io.BytesIO(file_data)

def validate_file_size(file_data: bytes, max_size: int) -> bool:
    """
    Valida tamanho do arquivo
    """
    return len(file_data) <= max_size

def get_file_extension(mime_type: str) -> str:
    """
    Retorna extensão baseada no MIME type
    """
    mime_to_ext = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'application/pdf': '.pdf'
    }
    return mime_to_ext.get(mime_type, '.bin')