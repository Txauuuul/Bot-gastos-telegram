"""
Guía para configurar las integraciones opcionales:
1. Google Cloud Vision API (OCR recomendado)
2. Google Drive (Sincronizar Excel)
"""

# =============================================================================
# OPCIÓN 1: GOOGLE CLOUD VISION API (OCR) - Recomendado
# =============================================================================

"""
Google Cloud Vision API es el mejor OCR disponible:
✅ Muy preciso (90%+ de exactitud)
✅ Maneja cualquier calidad de imagen
✅ Gratis: Crédito de $300 durante 12 meses
✅ No requiere nada instalado en tu PC

Pasos:
------

1. Crear proyecto en Google Cloud:
   - Ir a https://console.cloud.google.com
   - Crear proyecto nuevo (nombre libre)
   - Esperar a que se cree

2. Habilitar Vision API:
   - Abrir "APIs & Services" → "Library"
   - Buscar "Vision API"
   - Click en el resultado y presiona "Enable"

3. Crear credenciales:
   - Ir a "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Nombre: "telegram-bot-vision"
   - Skip los pasos opcionales
   - Crear cuenta de servicio
   - Click en la cuenta creada
   - Ir a "Keys" tab
   - "Add Key" → "Create new key" → JSON
   - Se descargará automáticamente (importante: ahí está tu clave)

4. Guardar credenciales:
   - Renombra el JSON descargado a: google-vision-key.json
   - Guarda en la carpeta del bot (mismo nivel que main.py)

5. Configurar en Python:
   - Establece variable de entorno:
   
   # En .env
   GOOGLE_APPLICATION_CREDENTIALS=./google-vision-key.json

   # O en Windows (PowerShell):
   $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\ruta\a\tu\bot\google-vision-key.json"
   python main.py

6. Instalar librería:
   pip install google-cloud-vision

7. Listo:
   - El bot usará automáticamente Vision API cuando envíes una foto
   - Si falla Vision, fallback a Tesseract
   - Si Tesseract no está, solo acepta texto manual

Estimación de costos:
---------------------
- Vision API: $1.50 por 1000 requests
- 30 fotos de tickets diarias = 900 al mes
- Costo: ~$1.35 al mes (gratis con crédito de $300)
- De hecho es gratis para la mayoría de usuarios

¿Es seguro compartir google-vision-key.json?
NO. Nunca lo subas a GitHub.
Ya está en .gitignore, pero ten cuidado.
Si lo expones, cualquiera puede usar tu cuota.


# =============================================================================
# OPCIÓN 2: GOOGLE DRIVE - Sincronizar Excel Automáticamente
# =============================================================================

"""
Sincroniza tu Excel gastos.xlsx automáticamente a Google Drive:
✅ Acceso 24/7 desde navegador
✅ Historial de versiones automático
✅ Compartir fácilmente con contable/familia
✅ Backup automático

Pasos:
------

1. Crear credenciales OAuth 2.0:
   - Ir a https://console.cloud.google.com
   - Abrir "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Si te pide, configura OAuth consent screen primero:
     * User type: "External"
     * Nombre app: "Mi Bot Tickets"
     * Email: Tu email
     * Guardar
   - De vuelta a Credentials:
   - Application type: "Desktop application"
   - Nombre: "telegram-bot-drive"
   - Create
   - Download JSON
   - Renombra a: credentials.json
   - Guarda en carpeta del bot

2. Instalar librerías:
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

3. Habilitar Google Drive API:
   - "APIs & Services" → "Library"
   - Buscar "Google Drive API"
   - Enable

4. Configurar en .env:
   USE_GOOGLE_DRIVE=true

5. Primera ejecución:
   python main.py
   - Se abrirá navegador pidiendo permiso
   - Permite acceso a Google Drive
   - Se genera token.json automáticamente
   - Excel se sube a Google Drive

6. Verificar:
   - Abre Google Drive
   - Busca "gastos.xlsx"
   - Debe estar ahí y actualizarse cada vez que agregas gasto

Compartir con otros:
-------------------
1. Abre Google Drive
2. Click derecho en gastos.xlsx
3. "Share"
4. Agrega emails de familia/contable
5. Listo, pueden ver en tiempo real

Advertencia importante:
---------------------
- Nunca subas credentials.json a GitHub
- Ya está en .gitignore, pero cuidado
- Si alguien lo obtiene, puede usar tu cuota de Drive
- El token.json se regenera automáticamente


# =============================================================================
# OPCIÓN 3: TESSERACT OCR (Local, Totalmente Gratis)
# =============================================================================

"""
OCR local sin internet, totalmente gratis pero menos preciso:

1. Descargar Tesseract:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Descargar el instalador .exe más reciente
   - Instalar en C:\Program Files\Tesseract-OCR (default)
   - Verificar en cmd: tesseract --version

2. Instalar Python packages:
   pip install pytesseract pillow

3. Configurar ruta en ocr_processor.py:
   Descomenta y configura (normalmente automático):
   # pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

4. Listo:
   - Usa automáticamente cuando envíes foto
   - Si Google Vision y Tesseract fallan, solo acepta texto

Precisión:
----------
- Tesseract (local): 70-80% con buenas fotos
- Google Vision: 95%+ incluso con mala iluminación
- Recomendación: Usar Vision para tickets, Tesseract como fallback


# =============================================================================
# RESUMEN: QUÉ INSTALAR
# =============================================================================

MÍNIMO (sin fotos, solo texto):
pip install -r requirements.txt

RECOMENDADO (fotos + GoogleDrive + Drive backup):
pip install -r requirements.txt
pip install google-cloud-vision

MÁXIMA COMPATIBILIDAD (fotos en local + nube + backup):
pip install -r requirements.txt
pip install google-cloud-vision pytesseract pillow

Luego configura credentials.json de Google para Drive.


# =============================================================================
# TESTING
# =============================================================================

Probar OCR:
python -c "from ocr_processor import extraer_texto_vision; print(extraer_texto_vision('ticket.jpg'))"

Probar parser:
from expense_parser import ExpenseParser
print(ExpenseParser.parse("Patatas 2.50€"))

Probar Excel:
from spreadsheet_manager import SpreadsheetManager
sm = SpreadsheetManager()
sm.agregar_gasto({"concepto": "Test", "precio": 1.0, "fecha": "19/02/2026", "hora": "10:00:00"})
"""

print(__doc__)
