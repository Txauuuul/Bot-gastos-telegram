"""
GUÍA RÁPIDA - CHECKLIST VISUAL
==============================

Sigue estos pasos en orden. Marca cada uno cuando lo termines.
Tiempo total: 15-20 minutos
"""

# =============================================================================
# CHECKLIST RÁPIDO
# =============================================================================

checklist = """

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    BOT TELEGRAM - CHECKLIST RÁPIDO                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


┌────────────────────────────────────────────────────────────────────────────┐
│ ⏱️  TIEMPO ESTIMADO: 15-20 MINUTOS                                         │
│                                                                             │
│ 📝 SIGUE TODOS LOS PASOS EN ORDEN                                         │
│ ✅ MARCA CADA PASO CUANDO LO TERMINES                                     │
└────────────────────────────────────────────────────────────────────────────┘


════════════════════════════════════════════════════════════════════════════
PASO 1: OBTENER TOKEN DE TELEGRAM (5 min)
════════════════════════════════════════════════════════════════════════════

⬜ Abre Telegram (móvil o web.telegram.org)
⬜ Busca @BotFather
⬜ Escribe /newbot
⬜ Elige nombre de bot (ej: Mi Bot Gastos)
⬜ Elige username del bot (ej: mi_bot_gastos_bot) - termina en _bot
⬜ COPIA el token (ejemplo: 123456:ABCdef-GHIjklmno...)
⬜ Guárdalo en un lugar seguro

🎯 RESULTADO: Tienes tu TOKEN listo


════════════════════════════════════════════════════════════════════════════
PASO 2: PREPARAR CARPETA (1 min)
════════════════════════════════════════════════════════════════════════════

⬜ Abre explorador: c:\\Users\\User\\Pop
⬜ Verifica que ves estos archivos:
   • main.py
   • expense_parser.py
   • requirements.txt
   • .env.example
   • instalar.bat
   • ejecutar.bat

🎯 RESULTADO: Estructura lista


════════════════════════════════════════════════════════════════════════════
PASO 3: CREAR ARCHIVO .env (3 min)
════════════════════════════════════════════════════════════════════════════

⬜ Abre VS Code (o Notepad)
⬜ Crea nuevo archivo (Ctrl+N)
⬜ Copia esto y REEMPLAZA el token:

   TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI_SIN_COMILLAS
   USE_GOOGLE_DRIVE=false
   WEBHOOK_URL=
   WEBHOOK_PORT=443
   WEBHOOK_SECRET=tu_password_secreto_aqui

Ejemplo:
   TELEGRAM_BOT_TOKEN=123456:ABCdef-GHIjklmno_PQRST-uvwxyz
   USE_GOOGLE_DRIVE=false
   WEBHOOK_URL=
   WEBHOOK_PORT=443
   WEBHOOK_SECRET=mysecret123

⬜ Guarda como ".env" en c:\\Users\\User\\Pop
⬜ Ctrl+Shift+S → Nombre: .env → Tipo: Todos los archivos (*)

🎯 RESULTADO: Archivo .env con tu token


════════════════════════════════════════════════════════════════════════════
PASO 4: INSTALAR LIBRERÍAS (5 min)
════════════════════════════════════════════════════════════════════════════

⬜ Abre terminal en VS Code (Ctrl+`)
⬜ Verifica que estés en: PS C:\\Users\\User\\Pop>
   (Si no, escribe: cd c:\\Users\\User\\Pop)

⬜ Instala pip:
   python -m pip install --upgrade pip
   [Presiona Enter, espera 1-2 min]

⬜ Instala librerías:
   pip install -r requirements.txt
   [Presiona Enter, espera 2-3 min]

⬜ Espera a ver: "Successfully installed..."

🎯 RESULTADO: Todas las librerías instaladas


════════════════════════════════════════════════════════════════════════════
PASO 5: EJECUTAR EL BOT (5 min)
════════════════════════════════════════════════════════════════════════════

⬜ En terminal, escribe:
   python main.py
   [Presiona Enter]

⬜ Espera a ver:
   INFO:__main__:🤖 Bot iniciado. Presiona Ctrl+C para detener.

⬜ Abre Telegram
   • Busca tu bot (@tu_usuario_bot)
   • O abre: t.me/tu_usuario_bot
   • Click "Iniciar" o "Start"

⬜ Prueba los comandos:
   
   TESTE 1:
   Escribe: /start
   Bot responde: ¡Hola! 👋 Bienvenido...
   
   TESTE 2:
   Escribe: Patatas 2.50€
   Bot responde: ✅ Gasto registrado...
   
   TESTE 3:
   Escribe: /resumen
   Bot responde: 📊 Resumen del Mes...

⬜ Verifica que se crea archivo:
   • En c:\\Users\\User\\Pop
   • Debe existir ahora: gastos.xlsx
   • Ábrelo, ve tus gastos registrados

🎯 RESULTADO: Bot funcionando perfectamente


════════════════════════════════════════════════════════════════════════════
PASO 6 (OPCIONAL): CONFIGURAR OCR PARA LEER TICKETS (15 min extra)
════════════════════════════════════════════════════════════════════════════

¿Quieres poder enviar FOTOS de tickets?

SI DICES NO:
⬜ Salta al FINAL (Paso 8)
⬜ Puedes configurar OCR después

SI DICES SI:
Elige UNA opción (recomiendo Google Vision):

────────────────────────────────────────────────────────────────────────────
OPCIÓN A: Google Cloud Vision (MEJOR - 95% precisión, gratis)
────────────────────────────────────────────────────────────────────────────

⬜ Abre: https://console.cloud.google.com
⬜ Crea proyecto nuevo:
   • "Select a Project" arriba izquierda
   • "New Project"
   • Nombre: "telegram-bot-tickets"
   • "Create"

⬜ Habilita Vision API:
   • "APIs & Services" → "Library"
   • Busca: "Vision API"
   • Click en el resultado
   • "ENABLE"

⬜ Crea credenciales:
   • "APIs & Services" → "Credentials"
   • "Create Credentials" → "Service Account"
   • Service account name: telegram-vision-bot
   • "Create and Continue"
   • "Continue" en los siguientes pasos
   • "Done"

⬜ Descarga JSON:
   • En "Credentials", busca la cuenta creada
   • Click en ella
   • Pestaña "KEYS"
   • "Add Key" → "Create new key" → "JSON"
   • Se descarga automáticamente
   • Renombra el archivo a: google-vision-key.json
   • Muévelo a: c:\\Users\\User\\Pop

⬜ Instala librería:
   pip install google-cloud-vision

⬜ Configura .env:
   • Abre .env
   • Añade esta línea:
   GOOGLE_APPLICATION_CREDENTIALS=./google-vision-key.json
   • Guarda (Ctrl+S)

⬜ Reinicia bot:
   • En terminal: Ctrl+C (para detenerlo)
   • python main.py (para reiniciarlo)

⬜ Prueba OCR:
   • En Telegram, envía una FOTO de ticket
   • El bot debe procesarla automáticamente
   • Debe extraer todos los gastos

────────────────────────────────────────────────────────────────────────────
OPCIÓN B: Tesseract (GRATIS, LOCAL, 70-80% precisión)
────────────────────────────────────────────────────────────────────────────

⬜ Descarga Tesseract:
   • Abre: https://github.com/UB-Mannheim/tesseract/wiki
   • Descarga el .exe más reciente
   • Ejecuta el instalador
   • Instala en: C:\\Program Files\\Tesseract-OCR
   • Next, Next, Install

⬜ Instala librerías:
   pip install pytesseract pillow

⬜ Reinicia bot:
   • En terminal: Ctrl+C
   • python main.py

⬜ Prueba OCR:
   • Envía foto de ticket a Telegram
   • El bot la procesa (más lento que Vision)

🎯 RESULTADO: Bot puede leer fotos de tickets


════════════════════════════════════════════════════════════════════════════
PASO 7 (OPCIONAL): SINCRONIZAR EXCEL CON GOOGLE DRIVE (10 min extra)
════════════════════════════════════════════════════════════════════════════

¿Quieres que Excel se suba automáticamente a Google Drive?

SI DICES NO:
⬜ Salta al FINAL (Paso 8)
⬜ Tu Excel está en local: c:\\Users\\User\\Pop\\gastos.xlsx
⬜ Puedes configurar Drive después

SI DICES SI:

⬜ Abre: https://console.cloud.google.com
   (Si estabas configurando Vision, usa el mismo proyecto)

⬜ Habilita Google Drive API:
   • "APIs & Services" → "Library"
   • Busca: "Google Drive API"
   • "ENABLE"

⬜ Crea OAuth credentials:
   • "APIs & Services" → "Credentials"
   • "Create Credentials" → "OAuth client ID"
   • Te pide configurar OAuth consent screen:
     - "External"
     - "Create"
     - App name: "Mi Bot Tickets"
     - User support email: tu email
     - Developer contact: tu email
     - "Save and Continue"
     - "Back to Dashboard"
   
   • De nuevo: "Create Credentials" → "OAuth client ID"
   • Application type: "Desktop application"
   • Name: "telegram-bot-drive"
   • "Create"
   • "Download JSON"
   • Renombra a: credentials.json
   • Muévelo a: c:\\Users\\User\\Pop

⬜ Instala librerías:
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

⬜ Configura .env:
   • Abre .env
   • Cambia: USE_GOOGLE_DRIVE=true
   • Guarda

⬜ Reinicia bot:
   • En terminal: Ctrl+C
   • python main.py
   • Se abrirá navegador pidiendo permiso
   • Autoriza acceso a "tu email" puede acceder a Drive
   • Se genera token.json automáticamente

⬜ Verifica en Google Drive:
   • Abre: drive.google.com
   • Busca: gastos.xlsx
   • Debe estar ahí
   • Se actualiza automáticamente con cada gasto nuevo

🎯 RESULTADO: Excel sincronizado con Google Drive 24/7


════════════════════════════════════════════════════════════════════════════
PASO 8: ¡LISTO!
════════════════════════════════════════════════════════════════════════════

✅ Bot funcionando en LOCAL
✅ Puedes escribir gastos manualmente
✅ Excel se crea automáticamente

Opcional (si lo configuraste):
✅ OCR para leer fotos de tickets
✅ Sincronización con Google Drive

🎉 ¡TU BOT ESTÁ LISTO!

════════════════════════════════════════════════════════════════════════════
PRÓXIMOS PASOS (CUANDO QUIERAS):
════════════════════════════════════════════════════════════════════════════

OPCIÓN A: Mantenerlo en tu PC
• Cada vez que quieras usar: python main.py
• Perfecto para desarrollo

OPCIÓN B: Pasar a PythonAnywhere (24/7 sin PC)
• Lee: GUIA_PYTHONANYWHERE.py
• Bot funcionará 24/7 en servidor
• Costo: ~$5/mes
• Acceso con teléfono desde cualquier lugar

════════════════════════════════════════════════════════════════════════════
❓ PROBLEMAS COMUNES Y SOLUCIONES:
════════════════════════════════════════════════════════════════════════════

❌ "TELEGRAM_BOT_TOKEN no encontrado"
✅ Solución: Verifica que .env existe y tiene el TOKEN

❌ "ModuleNotFoundError: No module named"
✅ Solución: pip install -r requirements.txt

❌ El bot no responde en Telegram
✅ Solución: Verifica que python main.py está corriendo
✅ Verifica que .env tiene el TOKEN correcto
✅ Verifica que tu bot existe en Telegram

❌ Las fotos no se procesan
✅ Solución: Instala OCR (Vision o Tesseract)
✅ Verifica que el archivo de credenciales está en la carpeta

❌ Excel no se crea
✅ Solución: Verifica que tienes openpyxl instalado
✅ pip install openpyxl

════════════════════════════════════════════════════════════════════════════
📞 ¿PREGUNTAS? 
════════════════════════════════════════════════════════════════════════════

Si algo no funciona:
1. Lee este checklist de nuevo
2. Lee GUIA_PASO_A_PASO.py para más detalles
3. Verifica los errores en la terminal
4. Pregúntame con el error específico

════════════════════════════════════════════════════════════════════════════
"""

print(checklist)

# Ahora mostramos opción para ejecutar la guía completa
print("\n")
print("¿Quieres la guía COMPLETA con más detalles?")
print("Ejecuta: python GUIA_PASO_A_PASO.py")
print("\nO sigue este verificador rápido. 👆")
