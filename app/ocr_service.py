import time
import logging
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from app.config import settings
from app.utils import create_file_object
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class AzureOCRService:
    def __init__(self):
        self.client = DocumentAnalysisClient(
            endpoint=settings.DI_ENDPOINT,
            credential=AzureKeyCredential(settings.DI_KEY)
        )
    
    async def analyze_document(self, file_data: bytes, model: str) -> Dict[str, Any]:
        """
        Analisa documento usando Azure OCR
        """
        start_time = time.time()
        
        try:
            # Criar objeto file-like
            file_obj = create_file_object(file_data)
            
            # Analisar documento
            logger.info(f"Iniciando análise com modelo: {model}")
            poller = self.client.begin_analyze_document(model, document=file_obj)
            result = poller.result()
            
            processing_time = time.time() - start_time
            logger.info(f"Análise concluída em {processing_time:.2f}s")
            
            # Processar resultado
            extracted_data = self._process_result(result, model)
            
            return {
                "success": True,
                "document_type": result.documents[0].doc_type if result.documents else None,
                "confidence": result.documents[0].confidence if result.documents else None,
                "extracted_data": extracted_data,
                "raw_response": self._serialize_result(result),
                "processing_time": processing_time
            }
            
        except AzureError as e:
            logger.error(f"Erro do Azure: {str(e)}")
            return {
                "success": False,
                "error": f"Erro do Azure OCR: {str(e)}",
                "processing_time": time.time() - start_time
            }
        except Exception as e:
            logger.error(f"Erro geral: {str(e)}")
            return {
                "success": False,
                "error": f"Erro interno: {str(e)}",
                "processing_time": time.time() - start_time
            }
    
    def _process_result(self, result, model: str) -> Dict[str, Any]:
        """
        Processa resultado baseado no modelo usado
        """
        if model == "prebuilt-receipt":
            return self._process_receipt(result)
        elif model == "prebuilt-invoice":
            return self._process_invoice(result)
        elif model == "prebuilt-layout":
            return self._process_layout(result)
        elif model == "prebuilt-businessCard":
            return self._process_business_card(result)
        elif model == "prebuilt-idDocument":
            return self._process_id_document(result)
        else:
            return self._process_generic(result)
    
    def _process_receipt(self, result) -> Dict[str, Any]:
        """Processa resultado de recibo"""
        extracted = {}
        
        if result.documents:
            doc = result.documents[0]
            if doc.fields:
                # Campos específicos de recibo
                fields_map = {
                    "MerchantName": "merchant_name",
                    "MerchantAddress": "merchant_address", 
                    "MerchantPhoneNumber": "merchant_phone",
                    "TransactionDate": "transaction_date",
                    "TransactionTime": "transaction_time",
                    "Items": "items",
                    "Subtotal": "subtotal",
                    "TotalTax": "tax",
                    "Tip": "tip",
                    "Total": "total"
                }
                
                for azure_field, our_field in fields_map.items():
                    if azure_field in doc.fields:
                        field = doc.fields[azure_field]
                        extracted[our_field] = {
                            "value": self._extract_field_value(field),
                            "confidence": field.confidence
                        }
        
        return extracted
    
    def _process_invoice(self, result) -> Dict[str, Any]:
        """Processa resultado de fatura"""
        # Implementar lógica específica para faturas
        return {"type": "invoice", "data": "invoice_data"}
    
    def _process_layout(self, result) -> Dict[str, Any]:
        """Processa resultado de layout"""
        extracted = {
            "pages": [],
            "tables": [],
            "text": []
        }
        
        # Processar páginas
        for page in result.pages:
            page_data = {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "unit": page.unit,
                "lines": []
            }
            
            for line in page.lines:
                page_data["lines"].append({
                    "content": line.content,
                    "confidence": getattr(line, 'confidence', None)
                })
            
            extracted["pages"].append(page_data)
        
        # Processar tabelas
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": []
            }
            
            for cell in table.cells:
                table_data["cells"].append({
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": cell.content
                })
            
            extracted["tables"].append(table_data)
        
        return extracted
    
    def _process_business_card(self, result) -> Dict[str, Any]:
        """Processa resultado de cartão de visita"""
        return {"type": "business_card", "data": "business_card_data"}
    
    def _process_id_document(self, result) -> Dict[str, Any]:
        """Processa resultado de documento de identidade"""
        return {"type": "id_document", "data": "id_document_data"}
    
    def _process_generic(self, result) -> Dict[str, Any]:
        """Processa resultado genérico"""
        return {"type": "generic", "data": "generic_data"}
    
    def _extract_field_value(self, field) -> Any:
        """Extrai valor do campo Azure"""
        if hasattr(field, 'value'):
            if hasattr(field.value, 'amount'):
                return field.value.amount
            return field.value
        return None
    
    def _serialize_result(self, result) -> Dict[str, Any]:
        """Serializa resultado para JSON"""
        try:
            return result.to_dict()
        except:
            return {"raw_result": "Unable to serialize"}