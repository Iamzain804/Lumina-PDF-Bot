@echo off
echo ========================================
echo   Stopping All Microservices
echo ========================================
echo.

echo Stopping Python processes...
taskkill /F /IM python.exe /T >nul 2>&1

echo Stopping Streamlit processes...
taskkill /F /IM streamlit.exe /T >nul 2>&1

echo.
echo All services stopped!
echo.
pause
