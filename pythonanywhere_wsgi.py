"""
Archivo para ejecutar el bot en PythonAnywhere como aplicación WSGI.
PythonAnywhere requiere una aplicación WSGI, este archivo la proporciona.

¿Cómo funciona?
1. Inicia la aplicación del bot (que corre en background)
2. Expone un endpoint WSGI para que PythonAnywhere pueda recibir webhooks
3. Telegram envía datos al webhook, se procesan y responden

Configuración en PythonAnywhere:
1. Crear Web app con Python 3.x y Flask
2. Reemplazar wsgi.py con este archivo
3. Apuntar la Web app a este archivo (pythonanywhere_wsgi.py)
4. El bot corre en background, los webhooks se procesan vía WSGI
"""

import os
import sys
import logging
from pathlib import Path

# Configurar rutas
PROJECT_DIR = str(Path(__file__).parent)
sys.path.insert(0, PROJECT_DIR)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables de entorno (PythonAnywhere las carga desde .env)
os.environ.setdefault('PYTHONUNBUFFERED', '1')

from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_DIR, '.env'))

from telegram import Update
from telegram.ext import Application
import json
import asyncio

# Obtener configuración
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    logger.error("⚠️  Variables de entorno no configuradas")
    logger.error("Asegúrate de que .env tiene: TELEGRAM_BOT_TOKEN y WEBHOOK_URL")

# Importar el bot (la aplicación se crea allí)
try:
    from main import application, MODE_NUBE
    logger.info("✅ Bot importado correctamente")
except ImportError as e:
    logger.error(f"❌ Error importando bot: {e}")
    application = None


# =============================================================================
# APLICACIÓN WSGI PARA PYTHONANYWHERE
# =============================================================================

async def handle_update(request_data):
    """Procesa un update de Telegram."""
    try:
        update = Update.de_json(request_data, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error procesando update: {e}")
        return {"status": "error", "message": str(e)}


def application_wsgi(environ, start_response):
    """Aplicación WSGI principal para PythonAnywhere."""
    
    # Solo procesar POST a /TOKEN
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(content_length)
            
            if request_body:
                request_data = json.loads(request_body.decode('utf-8'))
                
                # Procesar el update del bot usando asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(handle_update(request_data))
                loop.close()
                
                response = json.dumps(result).encode('utf-8')
                status = '200 OK'
            else:
                response = json.dumps({"status": "no_data"}).encode('utf-8')
                status = '200 OK'
                
        except Exception as e:
            logger.error(f"Error WSGI: {e}")
            response = json.dumps({"status": "error", "message": str(e)}).encode('utf-8')
            status = '500 Internal Server Error'
    else:
        # GET para verificar que está vivo
        response = json.dumps({
            "status": "alive",
            "webhook_url": WEBHOOK_URL,
            "mode": "webhook"
        }).encode('utf-8')
        status = '200 OK'
    
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response)))
    ]
    
    start_response(status, response_headers)
    return [response]


# Para que PythonAnywhere encuentre la aplicación WSGI
__all__ = ['application_wsgi']
