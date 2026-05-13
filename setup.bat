@echo off
REM Quick setup script for local development (Windows)
REM Run this script from the project root directory

echo.
echo === Flask Application Setup Script ===
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created at .\venv
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Copy environment file
echo Setting up environment configuration...
if not exist ".env" (
    copy .env.example .env
    echo .env file created from .env.example
    echo WARNING: Edit .env with your actual settings before deployment
) else (
    echo .env file already exists
)
echo.

REM Run tests
echo Running tests...
python -m pytest tests/ -v --tb=short
echo.

REM Summary
echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Edit .env with your settings
echo 2. Run the application: python app.py
echo 3. Open http://localhost:5000 in your browser
echo.
echo For AWS deployment:
echo 1. Push code to AWS CodeCommit
echo 2. Set up CodeBuild project
echo 3. Create CodePipeline
echo.
echo See AWS_SETUP_GUIDE.md for detailed instructions
echo.
pause
