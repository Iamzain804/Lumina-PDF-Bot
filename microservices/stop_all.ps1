# PowerShell Script to Stop All Microservices
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Stopping All Microservices" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Stopping Python processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "Stopping Streamlit processes..." -ForegroundColor Yellow
Get-Process streamlit -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host ""
Write-Host "✓ All services stopped!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
