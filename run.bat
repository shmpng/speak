@echo off
REM Quick start script for AI Speaking Coach (Windows)

echo 🗣️ Starting AI Speaking Coach...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Run the app
echo 🚀 Launching app...
echo 📱 Open your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run main.py
pause
