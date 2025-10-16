import base64
import requests
import json
import os

def test_single_pdf(pdf_filename):
    """Testa um PDF específico"""
    print(f"🔄 Testando: {pdf_filename}")
    
    # Verificar se arquivo existe
    if not os.path.exists(pdf_filename):
        print(f"❌ Arquivo não encontrado: {pdf_filename}")
        return
    
    try:
        # Ler arquivo
        with open(pdf_filename, "rb") as f:
            file_data = f.read()
        
        print(f"📄 Tamanho do arquivo: {len(file_data)} bytes")
        
        # Converter para base64
        file_base64 = base64.b64encode(file_data).decode()
        print(f"✅ Convertido para base64")
        
        # Preparar payload
        payload = {
            "file_data": file_base64,
            "file_type": "pdf",
            "model": "prebuilt-layout"  # Modelo para extrair layout
        }
        
        # Enviar para API
        print("🚀 Enviando para API...")
        response = requests.post("http://localhost:8000/analyze", json=payload)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCESSO!")
            
            if result.get('success'):
                print(f"⏱️ Tempo: {result.get('processing_time', 'N/A')}s")
                
                # Mostrar informações básicas
                extracted = result.get('extracted_data', {})
                if 'pages' in extracted:
                    pages = extracted['pages']
                    print(f"📄 Páginas processadas: {len(pages)}")
                    
                    # Mostrar primeira página
                    if pages:
                        first_page = pages[0]
                        lines = first_page.get('lines', [])
                        print(f"📝 Linhas na primeira página: {len(lines)}")
                        
                        # Mostrar algumas linhas
                        for i, line in enumerate(lines[:3]):
                            print(f"  {i+1}. {line.get('content', '')}")
                        if len(lines) > 3:
                            print(f"  ... e mais {len(lines) - 3} linhas")
                
                if 'tables' in extracted:
                    tables = extracted['tables']
                    print(f"📊 Tabelas encontradas: {len(tables)}")
                
                # Salvar resultado
                output_file = f"resultado_{pdf_filename.replace('.pdf', '')}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 Resultado salvo em: {output_file}")
                
            else:
                print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

# Listar PDFs na pasta
pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]

if pdf_files:
    print("📁 PDFs encontrados:")
    for i, file in enumerate(pdf_files, 1):
        print(f"{i}. {file}")
    
    print(f"\n🔄 Testando primeiro PDF: {pdf_files[0]}")
    test_single_pdf(pdf_files[0])
else:
    print("❌ Nenhum arquivo PDF encontrado na pasta atual")
    print("💡 Coloque seus PDFs na pasta ocr-api e execute novamente")

