import os
import base64
import requests
import json
from pathlib import Path

# URL da API
API_URL = "http://localhost:8000"

def list_files():
    """Lista arquivos PDF na pasta ocr-api/pdf"""
    pdf_folder = Path('pdf')
    
    # Criar pasta se não existir
    pdf_folder.mkdir(exist_ok=True)
    
    print("📁 Arquivos PDF encontrados em ocr-api/pdf:")
    pdf_files = list(pdf_folder.glob('*.pdf'))
    
    if not pdf_files:
        print("❌ Nenhum arquivo PDF encontrado na pasta pdf/")
        print("💡 Coloque seus arquivos PDF na pasta ocr-api/pdf/")
        return []
    
    for i, file in enumerate(pdf_files, 1):
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"{i}. {file.name} ({size_mb:.2f} MB)")
    
    return pdf_files

def test_pdf_file(file_path, model="prebuilt-layout"):
    """Testa um arquivo PDF específico"""
    print(f"\n🔄 Testando arquivo: {file_path}")
    print(f"📋 Modelo: {model}")
    
    try:
        # Ler arquivo
        with open(file_path, "rb") as f:
            file_data = f.read()
        
        # Converter para base64
        file_base64 = base64.b64encode(file_data).decode()
        print(f"✅ Arquivo convertido para base64 ({len(file_base64)} caracteres)")
        
        # Preparar payload
        payload = {
            "file_data": file_base64,
            "file_type": "pdf",
            "model": model
        }
        
        # Enviar para API
        print("🚀 Enviando para API...")
        response = requests.post(f"{API_URL}/analyze", json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCESSO!")
            
            if result.get('success'):
                print(f"Tempo de processamento: {result.get('processing_time', 'N/A')}s")
                
                # Mostrar dados extraídos baseado no modelo
                extracted_data = result.get('extracted_data', {})
                
                if model == "prebuilt-layout":
                    print("\n📊 Dados extraídos (Layout):")
                    if 'pages' in extracted_data:
                        pages = extracted_data['pages']
                        print(f"📄 Páginas: {len(pages)}")
                        
                        for page in pages[:2]:  # Mostrar apenas as 2 primeiras páginas
                            print(f"  Página {page.get('page_number', 'N/A')}: {len(page.get('lines', []))} linhas")
                    
                    if 'tables' in extracted_data:
                        tables = extracted_data['tables']
                        print(f"📊 Tabelas: {len(tables)}")
                        
                        for i, table in enumerate(tables[:2]):  # Mostrar apenas as 2 primeiras tabelas
                            print(f"  Tabela {i+1}: {table.get('row_count', 0)} linhas x {table.get('column_count', 0)} colunas")
                
                elif model == "prebuilt-receipt":
                    print("\n📊 Dados extraídos (Recibo):")
                    if 'merchant_name' in extracted_data:
                        merchant = extracted_data['merchant_name']
                        print(f"🏪 Comerciante: {merchant.get('value', 'N/A')}")
                    
                    if 'total' in extracted_data:
                        total = extracted_data['total']
                        print(f"💸 Total: ${total.get('value', 'N/A')}")
                
                # Salvar resultado completo
                output_file = f"resultado_{file_path.stem}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"💾 Resultado salvo em: {output_file}")
                
            else:
                print(f"❌ Erro na análise: {result.get('error', 'Erro desconhecido')}")
        else:
            print(f"❌ ERRO HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def interactive_test():
    """Teste interativo"""
    print("="*60)
    print("🧪 TESTE INTERATIVO - ARQUIVOS PDF")
    print("="*60)
    
    # Listar arquivos
    pdf_files = list_files()
    
    if not pdf_files:
        print("\n💡 Dica: Coloque seus arquivos PDF na pasta ocr-api/pdf/ e execute novamente")
        return
    
    # Escolher arquivo
    print(f"\n📋 Escolha um arquivo (1-{len(pdf_files)}):")
    try:
        choice = int(input("Digite o número: ")) - 1
        if 0 <= choice < len(pdf_files):
            selected_file = pdf_files[choice]
        else:
            print("❌ Escolha inválida")
            return
    except ValueError:
        print("❌ Digite um número válido")
        return
    
    # Escolher modelo
    print("\n🤖 Escolha o modelo:")
    print("1. prebuilt-layout (Layout e estrutura)")
    print("2. prebuilt-receipt (Recibos)")
    print("3. prebuilt-invoice (Faturas)")
    print("4. prebuilt-read (Apenas texto)")
    
    try:
        model_choice = int(input("Digite o número (1-4): "))
        models = {
            1: "prebuilt-layout",
            2: "prebuilt-receipt", 
            3: "prebuilt-invoice",
            4: "prebuilt-read"
        }
        model = models.get(model_choice, "prebuilt-layout")
    except ValueError:
        model = "prebuilt-layout"
    
    # Executar teste
    test_pdf_file(selected_file, model)

def quick_test_all():
    """Teste rápido de todos os PDFs com layout"""
    print("="*60)
    print("🚀 TESTE RÁPIDO - TODOS OS PDFs")
    print("="*60)
    
    pdf_files = list_files()
    
    if not pdf_files:
        print("❌ Nenhum arquivo PDF encontrado")
        return
    
    for file_path in pdf_files:
        test_pdf_file(file_path, "prebuilt-layout")
        print("-" * 40)

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Teste interativo (escolher arquivo e modelo)")
    print("2. Teste rápido (todos os PDFs com layout)")
    
    try:
        choice = int(input("Digite 1 ou 2: "))
        if choice == 1:
            interactive_test()
        elif choice == 2:
            quick_test_all()
        else:
            print("❌ Opção inválida")
    except ValueError:
        print("❌ Digite 1 ou 2")
    except KeyboardInterrupt:
        print("\n👋 Teste cancelado pelo usuário")
