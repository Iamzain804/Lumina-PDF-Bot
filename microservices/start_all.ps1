# PowerShell Script to Start All Microservices
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Lumina PDF Bot Microservices" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "[2/5] Starting Document Service (Port 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd document_service; python app.py" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[3/5] Starting Vector Service (Port 8002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd vector_service; python app.py" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[4/5] Starting LLM Service (Port 8003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd llm_service; python app.py" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[5/5] Starting Frontend Service (Port 8501)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend_service; streamlit run app.py" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All Services Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services Running:" -ForegroundColor Cyan
Write-Host "  - Document Service: http://localhost:8001" -ForegroundColor White
Write-Host "  - Vector Service:    http://localhost:8002" -ForegroundColor White
Write-Host "  - LLM Service:       http://localhost:8003" -ForegroundColor White
Write-Host "  - Frontend UI:       http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open Frontend..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Start-Process "http://localhost:8501"
