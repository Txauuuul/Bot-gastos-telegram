"""
GUÍA COMPLETA: Desplegar el Bot en PythonAnywhere (NUBE)

¿Qué es PythonAnywhere?
- Servidor en la nube donde Python corre 24/7
- No necesitas tu PC encendido
- Gratis hasta ciertos límites ($0-$5/mes)

Con esta configuración:
✅ Telegram envía datos directamente a PythonAnywhere
✅ El bot procesa y responde al instante
✅ Tu PC apagado? No importa, el bot funciona igual
✅ Fotos se suben a Google Drive automáticamente
"""

# =============================================================================
# PASO 1: Crear Cuenta en PythonAnywhere
# =============================================================================

"""
1. Abre https://www.pythonanywhere.com
2. "Pricing" → "Create a Beginner account" (gratis)
3. Regístrate con email
4. Verifica email
5. Abre el dashboard

Ya tienes tu URL de PythonAnywhere:
https://tunombre.pythonanywhere.com
"""

# =============================================================================
# PASO 2: Subir tu Código a PythonAnywhere
# =============================================================================

"""
OPCIÓN A: Vía Git (Recomendado)

1. En tu PC, abre la terminal y ve a la carpeta del bot:
   cd c:\Users\User\Pop

2. Inicializa git:
   git init
   git add .
   git commit -m "Bot inicial"

3. Crea repositorio en GitHub (gratis):
   - Abre https://github.com/new
   - Crea repo "telegram-bot-gastos"
   - Copia las instrucciones para subir código local
   
   En tu terminal:
   git remote add origin https://github.com/tunombre/telegram-bot-gastos.git
   git branch -M main
   git push -u origin main

4. En PythonAnywhere dashboard:
   - Abre Bash (terminal)
   - cd /home/tunombre
   - git clone https://github.com/tunombre/telegram-bot-gastos.git
   - cd telegram-bot-gastos

OPCIÓN B: Vía Upload Manual

1. En PythonAnywhere: Files → Upload
2. Sube todos los archivos .py
3. Sube requirements.txt
4. En Bash: pip install -r requirements.txt
"""

# =============================================================================
# PASO 3: Crear archivo .env en PythonAnywhere
# =============================================================================

"""
En PythonAnywhere:

1. Abre Files
2. Crea nuevo archivo: .env
3. Añade:

TELEGRAM_BOT_TOKEN=tu_token_de_botfather
USE_GOOGLE_DRIVE=true
WEBHOOK_URL=https://tunombre.pythonanywhere.com
WEBHOOK_PORT=443
WEBHOOK_SECRET=un_string_aleatorio_para_seguridad

Reemplaza:
- tunombre → tu nombre en PythonAnywhere
- tu_token_de_botfather → Tu token real
- un_string_aleatorio → Algo como: abc123xyz789
"""

# =============================================================================
# PASO 4: Instalar Dependencias en PythonAnywhere
# =============================================================================

"""
1. En PythonAnywhere: Web → Add a new web app
2. Python 3.x → Flask

3. Abre Bash y ejecuta:
   pip install -r requirements.txt
   pip install google-cloud-vision  # Si quieres OCR
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

# =============================================================================
# PASO 5: Configurar Web App en PythonAnywhere
# =============================================================================

"""
En PythonAnywhere dashboard:

1. Ir a Web
2. Add a new web app
   - Elegir Python 3.9 (o superior)
   - Manual configuration (no framework)
   
3. Una vez creada, editar WSGI configuration:
   - Abrir el archivo WSGI que sale por defecto
   - Reemplazar TODO el contenido con esto:

   ---
   import sys
   path = '/home/tunombre/telegram-bot-gastos'  # Reemplaza tunombre
   if path not in sys.path:
       sys.path.append(path)

   from pythonanywhere_wsgi import application_wsgi as application
   ---

4. Volver atrás y en "Code" añadir:
   - Source code: /home/tunombre/telegram-bot-gastos
   - Working directory: /home/tunombre/telegram-bot-gastos
   - WSGI configuration file: /var/www/tunombre_pythonanywhere_com_wsgi.py
   
5. RELOAD la web app (botón verde)

6. Verificar que funciona:
   - Abre https://tunombre.pythonanywhere.com en navegador
   - Debes ver JSON con {"status": "alive", ...}
"""

# =============================================================================
# PASO 6: Configurar Webhook en Telegram
# =============================================================================

"""
El webhook es la URL donde Telegram envía los mensajes.

OPCIÓN A: Vía Terminal (bash)

En PythonAnywhere Bash:
   curl -X POST https://api.telegram.org/botTU_TOKEN/setWebhook \
   -H 'Content-Type: application/json' \
   -d '{"url":"https://tunombre.pythonanywhere.com/TU_TOKEN"}'

Respuesta esperada:
   {"ok":true,"result":true,"description":"Webhook was set"}

OPCIÓN B: Script Helper

En terminal local o PythonAnywhere Bash:
   python setup_webhook.py

(El archivo setup_webhook.py está en la carpeta del bot)
"""

# =============================================================================
# PASO 7: Verificar que Funciona
# =============================================================================

"""
1. Abre tu bot en Telegram
2. Envía /start
3. El bot debe responder al instante
4. Envía una foto de un ticket
5. La foto se procesa y guarda en Excel en Google Drive

Si no funciona:
- En PythonAnywhere: Logs → Web → Ver error log
- Busca la línea de error
- Verifica que TELEGRAM_BOT_TOKEN esté correcto
- Verifica WEBHOOK_URL en .env
"""

# =============================================================================
# DIFERENCIAS: LOCAL vs NUBE
# =============================================================================

"""
MODO LOCAL (tu PC)
==================
python main.py
- Usa polling (pregunta constantemente a Telegram)
- Más lento
- Requiere PC encendido
- Mejor para desarrollo

MODO NUBE (PythonAnywhere)
==========================
Webhook automático
- Telegram envía msgs automáticamente
- Más rápido (responde al instante)
- Funciona sin PC encendido
- Mejor para producción

La detección es automática:
- Si WEBHOOK_URL en .env → MODO NUBE
- Si no → MODO LOCAL
"""

# =============================================================================
# ESTRUCTURA DE ARCHIVOS EN PYTHONANYWHERE
# =============================================================================

"""
/home/tunombre/telegram-bot-gastos/
├── main.py                     ← Bot principal
├── pythonanywhere_wsgi.py      ← Aplicación WSGI (importante)
├── expense_parser.py           ← Parser de gastos
├── spreadsheet_manager.py      ← Gestión Excel/Drive
├── ocr_processor.py            ← OCR
├── .env                        ← Secretos (no en git)
├── requirements.txt            ← Librerías
├── credentials.json            ← Google Drive (opcional)
├── token.json                  ← Token Drive (se genera)
└── gastos.xlsx                 ← Excel (se crea automáticamente)
"""

# =============================================================================
# COSTE Y LÍMITES
# =============================================================================

"""
PythonAnywhere Free:
- ✅ Dominio: tunombre.pythonanywhere.com
- ✅ 100MB almacenamiento
- ✅ 1 app web
- ✅ Perfectamente funcional para este bot
- Límite: Solo accesible 3 horas/día

PythonAnywhere Hacker ($5/mes):
- ✅ Acceso 24/7
- ✅ 512MB almacenamiento
- ✅ Base de datos incluida
- ✅ RECOMENDADO para usar el bot 24/7

Google Cloud Vision (OCR):
- ✅ Primeros 1000 requests al mes: GRATIS
- ✅ De 1000 en adelante: $1.50 por 1000
- Estimación: 30 fotos/día = ~$0.50/mes
"""

# =============================================================================
# SOLUCIÓN DE PROBLEMAS
# =============================================================================

"""
❌ "Webhook error"
→ WEBHOOK_URL en .env debe ser exacto: https://tunombre.pythonanywhere.com

❌ "ModuleNotFoundError"
→ pip install -r requirements.txt en PythonAnywhere Bash

❌ "Bot no responde"
→ Verificar Web app está RELOADED
→ Ver error logs en PythonAnywhere → Web → Logs

❌ "Google Drive no sincroniza"
→ Asegúrate que credentials.json está en el directorio
→ Ejecutar setup_google_drive.py para reautenticar

❌ "Image not accessible from URL"
→ Las imágenes se procesan en local, esto no debería ocurrir
→ Es un límite de telegram, las imágenes se descargan correctamente
"""

# =============================================================================
# PRÓXIMO PASO
# =============================================================================

"""
Una vez hayas seguido estos pasos:

1. El bot funciona en la nube 24/7
2. Puedes hacer fotos en el supermercado
3. Telegram etiqueta la foto
4. El bot la procesa automáticamente
5. Se guarda en Excel en Google Drive
6. Cuando abras el PC, el Excel ya está actualizado

¿Preguntas? Consúltame cualquier paso que no entiendas.
"""

print(__doc__)
