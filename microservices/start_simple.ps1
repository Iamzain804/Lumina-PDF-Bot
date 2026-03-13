# Start All Services with Virtual Environment
Write-Host "Starting Microservices..." -ForegroundColor Cyan

# Activate venv
$venvPath = "..\..\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "Virtual environment not found. Using system Python..." -ForegroundColor Yellow
}

# Start services
Write-Host "`nStarting Document Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\document_service'; python app.py"

Start-Sleep -Seconds 2

Write-Host "Starting Vector Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\vector_service'; python app.py"

Start-Sleep -Seconds 2

Write-Host "Starting LLM Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\llm_service'; python app.py"

Start-Sleep -Seconds 2

Write-Host "Starting Frontend Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend_service'; streamlit run app.py"

Write-Host "`n✅ All services started!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:8501" -ForegroundColor Cyan
