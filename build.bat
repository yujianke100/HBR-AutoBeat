@echo off
set SCRIPT_NAME=main.py
set OUTPUT_NAME=HBR-AutoBeat
set ICON_FILE=icon/favicon.ico

echo Checking uv installation...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv not found, installing uv...
    pip install uv
    if %errorlevel% neq 0 (
        echo Failed to install uv!
        pause
        exit /b %errorlevel%
    )
    echo uv installed successfully!
)

echo Setting up virtual environment with uv...
if not exist .venv (
    echo Creating virtual environment...
    uv venv
    if %errorlevel% neq 0 (
        echo Failed to create virtual environment!
        pause
        exit /b %errorlevel%
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment!
    pause
    exit /b %errorlevel%
)

echo Installing project dependencies from pyproject.toml...
uv pip install -e .
if %errorlevel% neq 0 (
    echo Failed to install dependencies from pyproject.toml!
    pause
    exit /b %errorlevel%
)

echo Verifying build dependencies...
if exist requirements-build.txt (
    echo Installing additional build requirements...
    uv pip install -r requirements-build.txt
    if %errorlevel% neq 0 (
        echo Failed to install build dependencies!
        pause
        exit /b %errorlevel%
    )
)

echo Verifying PyInstaller installation...
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found, installing...
    uv pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller!
        pause
        exit /b %errorlevel%
    )
)

echo Packaging %SCRIPT_NAME% as %OUTPUT_NAME%.exe...
pyinstaller --onefile --noconsole --name=%OUTPUT_NAME% --icon=%ICON_FILE% --hidden-import=yaml --add-data "i18n;i18n" --add-data "figs;figs" %SCRIPT_NAME%

if %errorlevel% neq 0 (
    echo error!
    pause
    exit /b %errorlevel%
)

echo Clearning tmp files...
rmdir /s /q build
del %OUTPUT_NAME%.spec

echo Success!
pause
