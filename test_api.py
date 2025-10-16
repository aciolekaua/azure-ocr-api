import requests
import base64
import json

# URL da API
API_URL = "http://localhost:8000"

def test_health():
    """Testa o endpoint de health"""
    print("🔍 Testando health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    print()

def test_models():
    """Lista modelos disponíveis"""
    print("📋 Listando modelos disponíveis...")
    response = requests.get(f"{API_URL}/models")
    print(f"Status: {response.status_code}")
    print(f"Modelos: {response.json()}")
    print()

def test_analyze_with_url():
    """Testa análise usando URL de imagem"""
    print("🔄 Testando análise com URL de imagem...")
    
    # URL de exemplo de um recibo
    receipt_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"
    
    # Converter URL para base64 (simulação)
    # Na prática, você faria: requests.get(url).content
    print(f"📄 Usando imagem de exemplo: {receipt_url}")
    
    # Para teste, vamos usar uma string base64 pequena como exemplo
    # Em produção, você converteria sua imagem real para base64
    test_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    payload = {
        "file_data": test_base64,
        "file_type": "image",
        "model": "prebuilt-receipt"
    }
    
    try:
        response = requests.post(f"{API_URL}/analyze", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Erro: {e}")
    print()

def test_analyze_with_real_image():
    """Testa análise com imagem real (se você tiver uma)"""
    print("📸 Para testar com imagem real:")
    print("1. Coloque uma imagem de recibo na pasta")
    print("2. Execute o código abaixo:")
    print()
    print("""
# Código para testar com imagem real:
import base64

# Ler sua imagem
with open("seu_recibo.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

payload = {
    "file_data": image_data,
    "file_type": "image", 
    "model": "prebuilt-receipt"
}

response = requests.post(f"{API_URL}/analyze", json=payload)
print(response.json())
""")

if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTE DA API AZURE OCR")
    print("="*60)
    print()
    
    # Testar health
    test_health()
    
    # Testar modelos
    test_models()
    
    # Testar análise
    test_analyze_with_url()
    
    # Instruções para teste real
    test_analyze_with_real_image()
    
    print("="*60)
    print("✅ Testes concluídos!")
    print("="*60)
