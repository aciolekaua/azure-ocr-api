import requests
import base64
import json

# URL da API
API_URL = "http://localhost:8000"

def test_with_real_receipt():
    """Testa com uma imagem real de recibo"""
    print("🔄 Testando com imagem real de recibo...")
    
    # URL de uma imagem real de recibo do Azure Samples
    receipt_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"
    
    try:
        # Baixar a imagem
        print("📥 Baixando imagem de exemplo...")
        response = requests.get(receipt_url)
        image_data = response.content
        
        # Converter para base64
        image_base64 = base64.b64encode(image_data).decode()
        print(f"✅ Imagem convertida para base64 ({len(image_base64)} caracteres)")
        
        # Preparar payload
        payload = {
            "file_data": image_base64,
            "file_type": "image",
            "model": "prebuilt-receipt"
        }
        
        # Enviar para API
        print("🚀 Enviando para API...")
        api_response = requests.post(f"{API_URL}/analyze", json=payload)
        
        print(f"Status Code: {api_response.status_code}")
        
        if api_response.status_code == 200:
            result = api_response.json()
            print("✅ SUCESSO!")
            print(f"Tipo de documento: {result.get('document_type', 'N/A')}")
            print(f"Confiança geral: {result.get('confidence', 'N/A')}")
            print(f"Tempo de processamento: {result.get('processing_time', 'N/A')}s")
            
            # Mostrar dados extraídos
            if result.get('extracted_data'):
                print("\n📊 Dados extraídos:")
                extracted = result['extracted_data']
                
                if 'merchant_name' in extracted:
                    merchant = extracted['merchant_name']
                    print(f"🏪 Comerciante: {merchant.get('value', 'N/A')} (confiança: {merchant.get('confidence', 'N/A')})")
                
                if 'total' in extracted:
                    total = extracted['total']
                    print(f"💸 Total: ${total.get('value', 'N/A')} (confiança: {total.get('confidence', 'N/A')})")
                
                if 'transaction_date' in extracted:
                    date = extracted['transaction_date']
                    print(f"📅 Data: {date.get('value', 'N/A')} (confiança: {date.get('confidence', 'N/A')})")
                
                if 'items' in extracted:
                    items = extracted['items']
                    print(f"🛒 Itens: {len(items.get('value', []))} itens encontrados")
        else:
            print(f"❌ ERRO: {api_response.status_code}")
            print(f"Resposta: {api_response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_with_your_image():
    """Instruções para testar com sua própria imagem"""
    print("\n" + "="*60)
    print("📸 PARA TESTAR COM SUA PRÓPRIA IMAGEM:")
    print("="*60)
    print()
    print("1. Coloque uma imagem de recibo na pasta ocr-api")
    print("2. Execute o código abaixo:")
    print()
    print("""
# Código para sua imagem:
import base64

# Ler sua imagem
with open("seu_recibo.jpg", "rb") as f:
    image_data = f.read()

# Converter para base64
image_base64 = base64.b64encode(image_data).decode()

# Enviar para API
payload = {
    "file_data": image_base64,
    "file_type": "image", 
    "model": "prebuilt-receipt"
}

response = requests.post("http://localhost:8000/analyze", json=payload)
print(response.json())
""")

if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTE DA API AZURE OCR - IMAGEM REAL")
    print("="*60)
    print()
    
    # Testar com imagem real
    test_with_real_receipt()
    
    # Instruções para teste próprio
    test_with_your_image()
    
    print("\n" + "="*60)
    print("✅ Teste concluído!")
    print("="*60)
