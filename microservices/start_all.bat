@echo off
echo ========================================
echo   Starting Lumina PDF Bot Microservices
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)

echo [1/5] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/5] Starting Document Service (Port 8001)...
start "Document Service" cmd /k "cd document_service && python app.py"
timeout /t 3 >nul

echo [3/5] Starting Vector Service (Port 8002)...
start "Vector Service" cmd /k "cd vector_service && python app.py"
timeout /t 3 >nul

echo [4/5] Starting LLM Service (Port 8003)...
start "LLM Service" cmd /k "cd llm_service && python app.py"
timeout /t 3 >nul

echo [5/5] Starting Frontend Service (Port 8501)...
start "Frontend Service" cmd /k "cd frontend_service && streamlit run app.py"
timeout /t 3 >nul

echo.
echo ========================================
echo   All Services Started Successfully!
echo ========================================
echo.
echo Services Running:
echo   - Document Service: http://localhost:8001
echo   - Vector Service:    http://localhost:8002
echo   - LLM Service:       http://localhost:8003
echo   - Frontend UI:       http://localhost:8501
echo.
echo Press any key to open Frontend...
pause >nul
start http://localhost:8501
