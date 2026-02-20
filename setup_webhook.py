"""
Script helper para configurar el webhook en Telegram.
Ejecutar una sola vez después de desplegar en PythonAnywhere.

Uso:
    python setup_webhook.py
"""

import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    print("❌ Error: TELEGRAM_BOT_TOKEN y WEBHOOK_URL deben estar en .env")
    print("\nEn .env debe haber:")
    print("TELEGRAM_BOT_TOKEN=tu_token")
    print("WEBHOOK_URL=https://tunombre.pythonanywhere.com")
    exit(1)

# Construir URL del webhook
webhook_full_url = f"{WEBHOOK_URL}/{TOKEN}"

print("=" * 60)
print("⚙️  Configurando webhook en Telegram")
print("=" * 60)
print(f"\nToken: {TOKEN[:20]}...")
print(f"Webhook URL: {webhook_full_url}")
print("\nEnviando solicitud a Telegram API...")

try:
    # Solicitar a la API de Telegram que configure el webhook
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {
        "url": webhook_full_url,
        "max_connections": 40,
        "allowed_updates": ["message", "callback_query"],
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("ok"):
        print("\n✅ ¡Webhook configurado exitosamente!")
        print(f"\nDetalles:")
        print(f"  Webhook URL: {webhook_full_url}")
        print(f"  Conexiones máximas: 40")
        print(f"  Mensajes a capturar: message, callback_query")
        
        # Obtener información del webhook configurado
        get_url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
        get_response = requests.post(get_url)
        webhook_info = get_response.json().get("result", {})
        
        print(f"\n📊 Estado del webhook:")
        print(f"  URL: {webhook_info.get('url', 'N/A')}")
        print(f"  Pendientes: {webhook_info.get('pending_update_count', 0)}")
        
    else:
        print(f"\n❌ Error configurando webhook:")
        print(f"  {result.get('description', 'Unknown error')}")
        exit(1)
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ Error de conexión: {e}")
    exit(1)

print("\n" + "=" * 60)
print("🎯 Próximos pasos:")
print("=" * 60)
print("""
1. Abre tu bot en Telegram
2. Envía /start
3. El bot debería responder al instante
4. Prueba enviando una foto o escribe "Patatas 2.50€"

Si no funciona:
- Verifica TELEGRAM_BOT_TOKEN en .env
- Verifica WEBHOOK_URL en .env
- Revisa los logs en PythonAnywhere
""")
