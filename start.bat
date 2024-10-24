@echo off
echo Checking Python installation...

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b
)

:: Check if required packages are installed
echo Checking required packages...
python -c "import faster_whisper" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install required packages.
        pause
        exit /b
    )
)

echo Starting Speech to Text Transcriber...
echo Press F2 to start/stop transcription, Ctrl+C to exit

:: Set OpenMP environment variable to avoid warnings
set KMP_DUPLICATE_LIB_OK=TRUE

:: Run the Python script
python main.py

:: If there's an error, pause to see it
if errorlevel 1 (
    echo An error occurred.
    pause
)