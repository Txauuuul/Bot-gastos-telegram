@echo off
REM Script de instalación automática para Windows
REM Instala todas las dependencias necesarias

echo.
echo ========================================
echo  Instalador del Bot de Gastos 📊
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en PATH
    echo Descarga desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Actualizar pip
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ Error actualizando pip
    pause
    exit /b 1
)

echo ✅ pip actualizado
echo.

REM Instalar dependencias base
echo 📥 Instalando librerías base...
pip install python-telegram-bot==20.7 python-dotenv==1.0.0 openpyxl==3.1.2

if %errorlevel% neq 0 (
    echo ❌ Error instalando librerías base
    pause
    exit /b 1
)

echo ✅ Librerías base instaladas
echo.

REM Instalación Opcional de Google Drive y Vision
setlocal enabledelayedexpansion
set /p opcion="¿Quieres instalar Google Cloud Vision (OCR recomendado)? (S/N): "

if /i "%opcion%"=="S" (
    echo 📥 Instalando Google Cloud Vision...
    pip install google-cloud-vision

    if !errorlevel! equ 0 (
        echo ✅ Google Cloud Vision instalado
    ) else (
        echo ⚠️  Error instalando Google Cloud Vision (opcional)
    )
    echo.
)

set /p drive="¿Quieres instalar sincronización con Google Drive? (S/N): "

if /i "%drive%"=="S" (
    echo 📥 Instalando Google Drive API...
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

    if !errorlevel! equ 0 (
        echo ✅ Google Drive instalado
    ) else (
        echo ⚠️  Error instalando Google Drive (opcional)
    )
    echo.
)

echo.
echo ========================================
echo  Instalación completada ✅
echo ========================================
echo.
echo Próximos pasos:
echo 1. Crea archivo .env con tu token:
echo    TELEGRAM_BOT_TOKEN=tu_token_aqui
echo.
echo 2. Ejecuta el bot:
echo    python main.py
echo.
echo Para más información, abre: README.md
echo.
pause
