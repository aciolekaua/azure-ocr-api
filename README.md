# Azure OCR API

API REST para análise de documentos usando Azure Document Intelligence (Form Recognizer). Esta API recebe arquivos em base64 e retorna dados estruturados extraídos dos documentos.

## 🚀 Funcionalidades

- 📄 Análise de recibos (comerciante, data, itens, total, impostos)
- 📋 Análise de layout de documentos (texto, tabelas, estrutura)
- 💳 Análise de cartões de visita
- 🆔 Análise de documentos de identidade
- 📊 Análise de faturas e notas fiscais
- 🎯 Alta precisão com níveis de confiança para cada campo
- 🌐 API REST com documentação automática

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Conta do Azure com recurso Document Intelligence ativo
- Credenciais do Azure (chave e endpoint)

## 🛠️ Configuração

### 1. Clone e configure

```bash
git clone <seu-repositorio>
cd ocr-api
```

### 2. Configure as credenciais

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Azure:

```env
DI_KEY=sua_chave_de_api_aqui
DI_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
```

**Como obter as credenciais:**

1. Acesse o [Azure Portal](https://portal.azure.com)
2. Navegue até seu recurso Azure AI Foundry ou Document Intelligence
3. Clique em **"Keys and Endpoint"** no menu lateral
4. Copie a **Key 1** (ou Key 2) e o **Endpoint**
5. Cole no arquivo `.env`

### 3. Execute com Docker

```bash
# Build e start dos containers
docker-compose up --build

# Ou em background
docker-compose up -d --build
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação da API

### Endpoints Disponíveis

#### `GET /health`
Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "azure-ocr-api",
  "version": "1.0.0"
}
```

#### `GET /models`
Lista os modelos OCR disponíveis.

**Resposta:**
```json
{
  "available_models": [
    "prebuilt-receipt",
    "prebuilt-invoice",
    "prebuilt-layout",
    "prebuilt-businessCard",
    "prebuilt-idDocument",
    "prebuilt-read"
  ]
}
```

#### `POST /analyze`
Analisa um documento usando Azure OCR.

**Request Body:**
```json
{
  "file_data": "base64_string_here",
  "file_type": "image|pdf",
  "model": "prebuilt-receipt|prebuilt-invoice|prebuilt-layout|prebuilt-businessCard|prebuilt-idDocument|prebuilt-read",
  "options": {}
}
```

**Resposta de Sucesso:**
```json
{
  "success": true,
  "document_type": "receipt.retailMeal",
  "confidence": 0.981,
  "extracted_data": {
    "merchant_name": {
      "value": "Contoso",
      "confidence": 0.989
    },
    "total": {
      "value": 2516.28,
      "confidence": 0.985
    },
    "transaction_date": {
      "value": "2019-06-10",
      "confidence": 0.995
    }
  },
  "raw_response": {...},
  "processing_time": 2.34
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "error": "Erro do Azure OCR: ...",
  "processing_time": 0.5
}
```

## 🔧 Exemplos de Uso

### Análise de Recibo

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "file_data": "iVBORw0KGgoAAAANSUhEUgAA...",
    "file_type": "image",
    "model": "prebuilt-receipt"
  }'
```

### Análise de Layout

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "file_data": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCg==",
    "file_type": "pdf",
    "model": "prebuilt-layout"
  }'
```

### Usando Python

```python
import requests
import base64

# Ler arquivo e converter para base64
with open("recibo.jpg", "rb") as f:
    file_data = base64.b64encode(f.read()).decode()

# Enviar para API
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "file_data": file_data,
        "file_type": "image",
        "model": "prebuilt-receipt"
    }
)

result = response.json()
print(f"Total: ${result['extracted_data']['total']['value']}")
```

## 📦 Modelos Disponíveis

| Modelo | Descrição | Campos Extraídos |
|--------|-----------|------------------|
| `prebuilt-receipt` | Recibos de vendas | Comerciante, data, itens, total, impostos |
| `prebuilt-invoice` | Faturas e notas fiscais | Fornecedor, cliente, itens, valores |
| `prebuilt-layout` | Layout e estrutura | Texto, tabelas, elementos visuais |
| `prebuilt-businessCard` | Cartões de visita | Nome, empresa, telefone, email |
| `prebuilt-idDocument` | Documentos de identidade | Nome, documento, data nascimento |
| `prebuilt-read` | Extração de texto (OCR) | Texto puro com coordenadas |

## 🐳 Comandos Docker

```bash
# Build da imagem
docker build -f docker/Dockerfile -t ocr-api .

# Executar container
docker run -p 8000:8000 --env-file .env ocr-api

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose down
docker-compose up --build --force-recreate
```

## 🔍 Monitoramento

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Logs em tempo real
docker-compose logs -f ocr-api

# Logs dos últimos 100 linhas
docker-compose logs --tail=100 ocr-api
```

## ❓ Troubleshooting

### Erro 404 - Resource not found
- ✅ Verifique se o endpoint está correto no arquivo `.env`
- ✅ Certifique-se de que o recurso existe no Azure Portal
- ✅ Confirme que está usando a biblioteca `azure-ai-formrecognizer==3.3.0`

### Erro de Autenticação
- ✅ Verifique se a chave está correta no arquivo `.env`
- ✅ Tente usar a Key 2 se a Key 1 não funcionar
- ✅ Confirme que o recurso está ativo no Azure

### Erro de Arquivo
- ✅ Verifique se o base64 está correto
- ✅ Confirme que o arquivo não excede 10MB
- ✅ Teste com arquivos menores primeiro

### Container não inicia
- ✅ Verifique se a porta 8000 está livre
- ✅ Confirme que o arquivo `.env` existe
- ✅ Execute `docker-compose logs` para ver erros

## 📁 Estrutura do Projeto

```
ocr-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # API FastAPI principal
│   ├── ocr_service.py       # Serviço Azure OCR
│   ├── models.py            # Modelos Pydantic
│   ├── utils.py             # Utilitários
│   └── config.py            # Configurações
├── docker/
│   └── Dockerfile
├── requirements.txt
├── .env                     # Credenciais (não commitar!)
├── .env.example
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## 🔒 Segurança

- **Não compartilhe** o arquivo `.env` com suas credenciais
- Use HTTPS em produção
- Configure CORS adequadamente para seu domínio
- Implemente rate limiting se necessário
- Monitore logs para detectar uso anômalo

## 📚 Recursos Adicionais

- [Documentação oficial do Azure Document Intelligence](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Azure AI Foundry](https://ai.azure.com/)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
