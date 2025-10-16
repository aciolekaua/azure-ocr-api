# Teste da API Azure OCR
$apiUrl = "http://localhost:8000"

Write-Host "🔍 Testando health check..." -ForegroundColor Green
$healthResponse = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get
Write-Host "Status: OK" -ForegroundColor Green
Write-Host "Resposta: $($healthResponse | ConvertTo-Json)" -ForegroundColor Yellow
Write-Host ""

Write-Host "📋 Listando modelos disponíveis..." -ForegroundColor Green
$modelsResponse = Invoke-RestMethod -Uri "$apiUrl/models" -Method Get
Write-Host "Modelos: $($modelsResponse | ConvertTo-Json)" -ForegroundColor Yellow
Write-Host ""

Write-Host "🔄 Testando análise com imagem de exemplo..." -ForegroundColor Green
$payload = @{
    file_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    file_type = "image"
    model = "prebuilt-receipt"
} | ConvertTo-Json

try {
    $analyzeResponse = Invoke-RestMethod -Uri "$apiUrl/analyze" -Method Post -Body $payload -ContentType "application/json"
    Write-Host "Status: Sucesso" -ForegroundColor Green
    Write-Host "Resposta: $($analyzeResponse | ConvertTo-Json -Depth 3)" -ForegroundColor Yellow
} catch {
    Write-Host "Erro: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Resposta: $($_.Exception.Response)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Testes concluídos!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan

