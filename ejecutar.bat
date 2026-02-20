@echo off
echo.
echo ========================================
echo  🤖 Bot de Gastos - Iniciando...
echo ========================================
echo.

REM Verificar que exista .env
if not exist .env (
    echo ❌ Archivo .env no encontrado
    echo.
    echo Crea un archivo .env con:
    echo TELEGRAM_BOT_TOKEN=tu_token_aqui
    echo.
    pause
    exit /b 1
)

REM Ejecutar bot
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error ejecutando el bot
    echo Presiona cualquier tecla para más información...
    pause
)
