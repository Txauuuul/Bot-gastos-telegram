"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           GUÍA COMPLETA: Bot de Telegram para Contabilidad               ║
║                     Paso a Paso desde CERO                                ║
║                                                                            ║
║           Versión: 1.0                                                   ║
║           Fecha: Febrero 2026                                            ║
║           Tiempo estimado: 15-20 minutos                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

print(__doc__)

# =============================================================================
# FASE 1: OBTENER TOKEN DE TELEGRAM (5 MINUTOS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 1: Obtener Token de Telegram                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

¿Qué es un TOKEN?
Es un código secreto que identifica a tu bot en Telegram.
Ejemplo: 123456:ABCdef-GHIjklmno_PQRST-uvwxyz

📋 INSTRUCCIONES:
═══════════════════════════════════════════════════════════════════════════

1️⃣  ABRE TELEGRAM
    └─ En tu móvil o en https://web.telegram.org

2️⃣  ENCUENTRA A @BotFather
    └─ En la barra de búsqueda, escribe: @BotFather
    └─ Es el bot oficial de Telegram para crear bots

3️⃣  INICIA CONVERSACIÓN
    └─ Click en @BotFather
    └─ Presiona "Start"

4️⃣  CREA UN BOT NUEVO
    └─ Escribe exactamente esto: /newbot
    └─ BotFather te preguntará por el nombre

5️⃣  ELIGE NOMBRE PARA TU BOT
    └─ Nombre visible (lo que ven otros)
    └─ Ejemplo: "Mi Bot de Gastos"
    └─ Escribe y presiona Enter

6️⃣  ELIGE USERNAME DEL BOT
    └─ Debe terminar en _bot
    └─ Ejemplo: mi_bot_gastos_bot
    └─ Debe ser ÚNICO (sin espacios, solo letras, números y _)

7️⃣  COPIAR EL TOKEN
    └─ BotFather te muestra algo como:
    
    ╔═══════════════════════════════════════════════════════════════════╗
    ║ Done! Congratulations on your new bot. You will find it at       ║
    ║ t.me/tu_nombre_bot                                              ║
    ║ You can now add a description, about section and commands.       ║
    ║                                                                   ║
    ║ Token: 123456:ABCdef-GHIjklmno_PQRST-uvwxyz                      ║
    ║                                                                   ║
    ║ Use this token to access the HTTP API                            ║
    ║ Keep your token secure and store it safely!                      ║
    ╚═══════════════════════════════════════════════════════════════════╝
    
    └─ COPIA el token (es el número:XXXXX)
    └─ GUÁRDALO en un lugar seguro (lo usarás en el siguiente paso)
    └─ NO lo compartas con nadie

✅ FASE 1 COMPLETADA
Tienes tu token de Telegram.

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER cuando tengas el token listo...")

# =============================================================================
# FASE 2: PREPARAR CARPETA DEL PROYECTO (2 MINUTOS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 2: Verificar Estructura de Carpetas                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

La carpeta c:\\Users\\User\\Pop debería contener ESTOS archivos:

📁 c:\\Users\\User\\Pop\\
├── main.py                          ← Bot principal (YA EXISTE)
├── expense_parser.py                ← Parser de gastos (YA EXISTE)
├── spreadsheet_manager.py           ← Gestor de Excel (YA EXISTE)
├── ocr_processor.py                 ← OCR de imágenes (YA EXISTE)
├── pythonanywhere_wsgi.py          ← Para nube (YA EXISTE)
├── requirements.txt                 ← Librerías (YA EXISTE)
├── .env.example                     ← Plantilla (YA EXISTE)
├── .gitignore                       ← Para git (YA EXISTE)
├── README.md                        ← Documentación (YA EXISTE)
├── GUIA_PYTHONANYWHERE.py          ← Guía nube (YA EXISTE)
├── setup_webhook.py                 ← Configurador webhook (YA EXISTE)
├── SETUP_INTEGRACIONES.py          ← Integraciones (YA EXISTE)
├── instalar.bat                     ← Instalador (YA EXISTE)
├── ejecutar.bat                     ← Lanzador (YA EXISTE)
└── .env                             ← ⭐ LO CREARÁS AHORA (NO EXISTE)

VERIFICACIÓN:
═══════════════════════════════════════════════════════════════════════════

1️⃣  Abre el explorador de archivos
    └─ Escribe en la barra: c:\\Users\\User\\Pop
    └─ Presiona Enter

2️⃣  Verifica que ves estos archivos:
    ✓ main.py
    ✓ expense_parser.py
    ✓ requirements.txt
    ✓ .env.example
    ✓ instalar.bat
    ✓ ejecutar.bat

✅ FASE 2 COMPLETADA
Estructura lista.

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER para continuar...")

# =============================================================================
# FASE 3: CREAR ARCHIVO .env (3 MINUTOS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 3: Crear Archivo .env (Configuración Secreta)                       ║
╚════════════════════════════════════════════════════════════════════════════╝

¿Qué es .env?
Es un archivo que guarda datos secretos (tu token) SIN mostrarlos en el código.
NO se sube a internet, está protegido en .gitignore.

📋 INSTRUCCIONES:
═══════════════════════════════════════════════════════════════════════════

1️⃣  ABRE VS CODE
    └─ O cualquier editor de texto (Notepad, etc.)

2️⃣  CREA UN ARCHIVO NUEVO
    └─ En VS Code: Ctrl+N
    └─ O Archivo → Nuevo

3️⃣  COPIA EXACTAMENTE ESTO:

┌───────────────────────────────────────────────────────────────────────────┐
│ TELEGRAM_BOT_TOKEN=AQUI_TU_TOKEN_SIN_COMILLAS                            │
│ USE_GOOGLE_DRIVE=false                                                   │
│ WEBHOOK_URL=                                                             │
│ WEBHOOK_PORT=443                                                         │
│ WEBHOOK_SECRET=tu_password_secreto_aqui                                  │
└───────────────────────────────────────────────────────────────────────────┘

4️⃣  REEMPLAZA "AQUI_TU_TOKEN_SIN_COMILLAS"
    └─ Con el token que copiaste de BotFather
    └─ Ejemplo completo:
    
    TELEGRAM_BOT_TOKEN=123456:ABCdef-GHIjklmno_PQRST-uvwxyz
    USE_GOOGLE_DRIVE=false
    WEBHOOK_URL=
    WEBHOOK_PORT=443
    WEBHOOK_SECRET=mi_secreto_123

5️⃣  GUARDA EL ARCHIVO
    └─ En VS Code: Ctrl+Shift+S (Guardar Como)
    └─ Nombre: .env (exactamente así, con el punto)
    └─ Ubicación: c:\\Users\\User\\Pop
    └─ Tipo: Todos los archivos (*)
    └─ Presiona "Guardar"

⚠️  IMPORTANTE:
  • El archivo se llama .env (comienza con punto)
  • Debe estar en la MISMA CARPETA que main.py
  • NO lo compartas, NO lo subas a GitHub
  • Ya está protegido en .gitignore

✅ FASE 3 COMPLETADA
Archivo .env creado con tu token.

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER cuando hayas creado .env...")

# =============================================================================
# FASE 4: INSTALAR DEPENDENCIAS (5 MINUTOS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 4: Instalar Librerías Python                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

¿Qué son dependencias?
Son librerías (código reutilizable) que necesita tu bot para funcionar.

📋 INSTRUCCIONES:
═══════════════════════════════════════════════════════════════════════════

1️⃣  ABRE LA TERMINAL DE VS CODE
    └─ En VS Code: Ctrl+` (backtick, debajo de Esc)
    └─ O: Terminal → New Terminal
    └─ Debe abrir una ventana negra en la parte inferior

2️⃣  VERIFICA QUE ESTÁS EN LA CARPETA CORRECTA
    └─ En la terminal debe decir:
    
    PS C:\\Users\\User\\Pop>
    
    └─ Si NO está así, escribe:
    
    cd c:\\Users\\User\\Pop
    
    └─ Y presiona Enter

3️⃣  ACTUALIZAR PIP (Gestor de librerías)
    └─ Copia esto exactamente:
    
    python -m pip install --upgrade pip
    
    └─ Presiona Enter
    └─ Espera a que termine (1-2 minutos)
    └─ Verás al final: "Successfully installed..."

4️⃣  INSTALAR TODAS LAS LIBRERÍAS
    └─ Copia esto exactamente:
    
    pip install -r requirements.txt
    
    └─ Presiona Enter
    └─ Espera a que termine (2-3 minutos)
    └─ Verás al final: "Successfully installed..."

⌚  ESPERA PACIENCIA - Esto puede tardar 2-3 minutos

5️⃣  VERIFICA QUE FUNCIONÓ
    └─ Si ves "Successfully installed" → ✅ Listo
    └─ Si ves errores en rojo → ❌ Reportamelo

✅ FASE 4 COMPLETADA
Todas las librerías instaladas.

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER cuando termines la instalación...")

# =============================================================================
# FASE 5: PROBAR EL BOT EN LOCAL (5 MINUTOS)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 5: Ejecutar el Bot por Primera Vez                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Ahora test del bot en tu PC (modo LOCAL, polling).

📋 INSTRUCCIONES:
═══════════════════════════════════════════════════════════════════════════

1️⃣  EN LA TERMINAL, ESCRIBE:
    
    python main.py
    
    └─ Presiona Enter

2️⃣  ESPERA A VER ESTO:
    
    INFO:__main__:🤖 Bot iniciado. Presiona Ctrl+C para detener.
    
    └─ Si lo ves → ✅ El bot está corriendo
    └─ Si ves errores → ❌ Revisa que .env esté correcto

3️⃣  ABRE TELEGRAM
    └─ Busca tu bot (@tu_nombre_bot)
    └─ O usa este link: t.me/tu_nombre_bot
    └─ Click en "Iniciar" o "Start"

4️⃣  ENVÍA COMANDOS AL BOT
    
    Prueba 1: Comando /start
    ┌────────────────────────────────┐
    │ Tú: /start                     │
    │                                │
    │ Bot: ¡Hola! 👋                 │
    │      Bienvenido a tu bot...    │
    │      Estoy listo para...       │
    └────────────────────────────────┘
    
    Prueba 2: Escribir un gasto
    ┌────────────────────────────────┐
    │ Tú: Patatas 2.50€              │
    │                                │
    │ Bot: ✅ Gasto registrado:       │
    │      • Concepto: Patatas       │
    │      • Precio: 2.50€           │
    │      • Fecha: 19/02/2026...    │
    └────────────────────────────────┘
    
    Prueba 3: Ver resumen
    ┌────────────────────────────────┐
    │ Tú: /resumen                   │
    │                                │
    │ Bot: 📊 Resumen del Mes        │
    │      💰 Total: 2.50€           │
    │      🧾 Gastos: 1              │
    │      📈 Promedio: 2.50€        │
    └────────────────────────────────┘

5️⃣  VERIFICA QUE SE CREA EXCEL
    └─ En la carpeta c:\\Users\\User\\Pop
    └─ Debe aparecer un archivo: gastos.xlsx
    └─ Ábrelo en Excel o Google Sheets
    └─ Debe tener tus gastos registrados

✅ PRUEBAS BÁSICAS COMPLETADAS
El bot funciona correctamente en LOCAL.

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER para continuar...")

# =============================================================================
# FASE 6: OPTIONAL - CONFIGURAR OCR (15 MINUTOS EXTRA)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 6 (OPCIONAL): Configurar OCR para Leer Tickets                       ║
╚════════════════════════════════════════════════════════════════════════════╝

¿Qué es OCR?
Optical Character Recognition = La máquina lee texto de fotos.
El bot puede analizar automáticamente fotos de tickets.

✋ PAUSA AQUÍ
Antes de continuar, responde:
¿Quieres poder enviar FOTOS de tickets ahora, o solo texto por ahora?

OPCIÓN A: Solo texto por ahora (2.50€ escrito a mano)
└─ Salta al FINAL y termina
└─ Más adelante puedes agregar OCR

OPCIÓN B: Quiero OCR ahora (leer fotos de tickets automáticamente)
└─ Continúa leyendo

Si elegiste OPCIÓN B, tienes 2 alternativas:

═══════════════════════════════════════════════════════════════════════════
ALTERNATIVA 1: Google Cloud Vision (RECOMENDADO - 95% precisión)
═══════════════════════════════════════════════════════════════════════════

✅ Ventajas:
  • Muy preciso (95%+ de precisión)
  • Gratis primeros 1000 requests/mes
  • Maneja cualquier calidad de foto
  • Funciona desde cualquier lugar

❌ Desventajas:
  • Requiere cuenta de Google Cloud
  • Tomar 10 minutos configurar

📋 INSTRUCCIONES:
───────────────────────────────────────────────────────────────────────────

1️⃣  IR A GOOGLE CLOUD CONSOLE
    └─ Abre https://console.cloud.google.com
    └─ Si no tienes cuenta de Google, créala (gratis)

2️⃣  CREAR PROYECTO NUEVO
    └─ Arriba a la izquierda, verás "Select a Project"
    └─ Click en él
    └─ "New Project"
    └─ Nombre: "telegram-bot-tickets"
    └─ Presiona "Create"
    └─ Espera 1-2 minutos

3️⃣  HABILITAR VISION API
    └─ Una vez creado el proyecto, ve a "APIs & Services"
    └─ Click "Library"
    └─ Busca: "Vision API"
    └─ Presiona el resultado "Cloud Vision API"
    └─ Click "ENABLE"
    └─ Espera a que se habilite

4️⃣  CREAR CREDENCIALES
    └─ Ve a "APIs & Services" → "Credentials"
    └─ Arriba, click "Create Credentials"
    └─ Elige "Service Account"
    └─ Datos:
      • Service account name: telegram-vision-bot
      • Service account ID: auto
      • Leave description empty
    └─ Click "Create and Continue"
    └─ Click "Continue" en los siguientes pasos
    └─ Click "Done"

5️⃣  CREAR Y DESCARGAR CLAVE
    └─ Vas a "Credentials" de nuevo
    └─ Bajo "Service Accounts", verás la cuenta que creaste
    └─ Click en ella
    └─ Ve a la pestaña "KEYS"
    └─ "Add Key" → "Create new key"
    └─ Tipo: "JSON"
    └─ Click "Create"
    └─ Se descarga automáticamente un archivo JSON
    └─ IMPORTANTE: Renómbralo a: google-vision-key.json
    └─ Muévelo a c:\\Users\\User\\Pop

6️⃣  INSTALAR LIBRERÍA
    └─ En la terminal de VS Code, ejecuta:
    
    pip install google-cloud-vision
    
    └─ Presiona Enter
    └─ Espera a que termine

7️⃣  CONFIGURAR VARIABLE DE ENTORNO
    └─ Abre tu archivo .env
    └─ Añade esta línea:
    
    GOOGLE_APPLICATION_CREDENTIALS=./google-vision-key.json
    
    └─ Guarda (Ctrl+S)

8️⃣  PRUEBA OCR
    └─ En la terminal, detén el bot: Ctrl+C
    └─ Ejecuta de nuevo: python main.py
    └─ Envía una foto de un ticket a tu bot
    └─ El bot debe procesarla automáticamente

═══════════════════════════════════════════════════════════════════════════
ALTERNATIVA 2: Tesseract (Local, Gratis, Menos Preciso)
═══════════════════════════════════════════════════════════════════════════

✅ Ventajas:
  • Totalmente gratis
  • Funciona sin internet
  • 70-80% de precisión (aceptable)

❌ Desventajas:
  • Requiere instalar programa adicional
  • Más lento
  • Peor precisión que Vision

📋 INSTRUCCIONES:
───────────────────────────────────────────────────────────────────────────

1️⃣  DESCARGAR TESSERACT
    └─ Abre: https://github.com/UB-Mannheim/tesseract/wiki
    └─ Busca "Downloads"
    └─ Link: "Tesseract installer for Windows"
    └─ Descarga: tesseract-ocr-w64-setup-v5.x.x.exe
    └─ Ejecuta el instalador
    └─ Acepta todo (next, next, next, install)
    └─ Instala en ubicación por defecto: C:\\Program Files\\Tesseract-OCR

2️⃣  INSTALAR LIBRERÍAS PYTHON
    └─ En la terminal, ejecuta:
    
    pip install pytesseract pillow
    
    └─ Presiona Enter

3️⃣  PRUEBA OCR
    └─ Detén el bot: Ctrl+C
    └─ Ejecuta: python main.py
    └─ Envía una foto de ticket
    └─ El bot la procesará (más lento que Vision)

═══════════════════════════════════════════════════════════════════════════
RECOMENDACIÓN:
Google Cloud Vision (Opción 1) es mejor, pero toma más tiempo configurar.
Tesseract (Opción 2) es rápido pero menos preciso.

Para este proyecto, RECOMIENDO Google Cloud Vision.

═══════════════════════════════════════════════════════════════════════════
""")

# =============================================================================
# FASE 7: OPTIONAL - GOOGLE DRIVE (10 MINUTOS EXTRA)
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ FASE 7 (OPCIONAL): Sincronizar Excel a Google Drive                      ║
╚════════════════════════════════════════════════════════════════════════════╝

¿Qué es esto?
Tu Excel gastos.xlsx se sube automáticamente a Google Drive.
Puedes verlo desde móvil, tablet, etc. 24/7, siempre actualizado.

¿Lo quieres ahora?
Si dices SÍ, toma 10 minutos extra configurar.
Si dices NO, lo haces cuando quieras más adelante.

Responde en la siguiente pregunta...

""")

quiero_drive = input("¿Quieres sincronizar con Google Drive ahora? (S/N): ").lower().strip()

if quiero_drive == 's':
    print("""
    
📋 INSTRUCCIONES GOOGLE DRIVE:
═══════════════════════════════════════════════════════════════════════════

1️⃣  IR A GOOGLE CLOUD CONSOLE (de nuevo)
    └─ Abre https://console.cloud.google.com
    └─ Asegúrate de estar en el proyecto que creaste

2️⃣  HABILITAR GOOGLE DRIVE API
    └─ Ve a "APIs & Services" → "Library"
    └─ Busca: "Google Drive API"
    └─ Presiona el resultado
    └─ Click "ENABLE"

3️⃣  CREAR CREDENCIALES OAuth
    └─ Ve a "APIs & Services" → "Credentials"
    └─ Click "Create Credentials" → "OAuth client ID"
    └─ Te pide configurar "OAuth consent screen"
    └─ Elige "External"
    └─ Click "Create"
    └─ Datos:
      • App name: "Mi Bot Tickets"
      • User support email: tu email
      • Developer email: tu email
    └─ Click "Save and Continue"
    └─ Skip los siguientes pasos
    └─ Click "Back to Dashboard"
    
4️⃣  CREAR ClientID
    └─ De nuevo en "Credentials"
    └─ "Create Credentials" → "OAuth client ID"
    └─ Application type: "Desktop application"
    └─ Name: "telegram-bot-drive"
    └─ Click "Create"
    └─ Click "Download JSON"
    └─ Renombra a: credentials.json
    └─ Muévelo a c:\\Users\\User\\Pop

5️⃣  INSTALAR LIBRERÍAS
    └─ En terminal:
    
    pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
    
    └─ Presiona Enter

6️⃣  HABILITAR EN .env
    └─ Abre .env
    └─ Cambia:
    
    USE_GOOGLE_DRIVE=true
    
    └─ Guarda

7️⃣  PRIMERA EJECUCIÓN
    └─ En terminal: Ctrl+C (si está corriendo)
    └─ Ejecuta: python main.py
    └─ Se abrirá navegador pidiendo permiso
    └─ Autoriza acceso a Google Drive
    └─ Se genera token.json automáticamente
    └─ El bot está listo

8️⃣  VERIFICAR
    └─ Abre Google Drive (drive.google.com)
    └─ Busca "gastos.xlsx"
    └─ Debe estar ahí
    └─ Cada gasto nuevo se sube automáticamente

✅ GOOGLE DRIVE CONFIGURADO

═══════════════════════════════════════════════════════════════════════════
    """)
else:
    print("""
    
✅ SALTANDO GOOGLE DRIVE
   Puedes configurarlo más adelante cuando quieras.
   
═══════════════════════════════════════════════════════════════════════════
    """)

# =============================================================================
# RESUMEN FINAL
# =============================================================================

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║ ✅ INSTALACIÓN COMPLETADA                                                ║
╚════════════════════════════════════════════════════════════════════════════╝

Tu bot de Telegram está configurado y funcionando.

═══════════════════════════════════════════════════════════════════════════
📋 RESUMEN DE LO QUE HICISTE:
═══════════════════════════════════════════════════════════════════════════

✅ Obtuviste token de Telegram
✅ Creaste archivo .env con configuración
✅ Instalaste todas las librerías necesarias
✅ Ejecutaste el bot con éxito
✅ Probaste comandos (/start, /resumen)
✅ Registraste gastos manualmente
✅ Excel se crea automáticamente

Opcional (si lo hiciste):
✅ Configuraste OCR para leer fotos
✅ Sincronizaste Excel con Google Drive

═══════════════════════════════════════════════════════════════════════════
🎯 AHORA PUEDES:
═══════════════════════════════════════════════════════════════════════════

LÍNEA DE COMANDOS:
  /start      → Ver bienvenida
  /resumen    → Ver gastos del mes
  /ayuda      → Ver todos los comandos

ESCRIBIR GASTOS:
  "Patatas 2.50€"     → Se registra automáticamente
  "Leche: 1.20€"      → Cualquier formato funciona
  "3.45€ Manzanas"    → Flexible

ENVIAR FOTOS (si configuraste OCR):
  Foto de ticket → Bot la analiza automáticamente
              → Extrae gastos
              → Los guarda en Excel

SINCRONIZAR:
  Excel se sube a Google Drive automáticamente
  Accesible desde cualquier dispositivo

═══════════════════════════════════════════════════════════════════════════
📁 ARCHIVOS IMPORTANTES:
═══════════════════════════════════════════════════════════════════════════

  .env                    ← Tu configuración secreta (NO COMPARTIR)
  gastos.xlsx             ← Tu Excel con gastos (generado automáticamente)
  main.py                 ← El bot (no editar)
  google-vision-key.json  ← Tu API key (si configuraste OCR)
  credentials.json        ← Tu Drive credentials (si configuraste Drive)

═══════════════════════════════════════════════════════════════════════════
🚀 PRÓXIMOS PASOS OPCIONALES:
═══════════════════════════════════════════════════════════════════════════

OPCIÓN 1: Dejar el bot en tu PC
  • Ejecuta: python main.py
  • Debe estar encendido para que funcione
  • Perfecto para desarrollo/testing

OPCIÓN 2: Pasar a PythonAnywhere (RECOMENDADO)
  • Bot corre en servidor 24/7
  • No necesitas PC encendido
  • Fotos en supermercado → Bot procesa automáticamente
  • Instrucciones: Lee GUIA_PYTHONANYWHERE.py
  • Costo: ~$5/mes (gratis 3 horas al día)

═══════════════════════════════════════════════════════════════════════════
❓ DUDAS COMUNES:
═══════════════════════════════════════════════════════════════════════════

P: ¿El bot necesita mi PC encendido?
R: SÍ en LOCAL. NO si lo subes a PythonAnywhere.

P: ¿Pueden hackear mi token?
R: No está en .env (está en .gitignore). Está seguro.

P: ¿Cuánto cuesta?
R: Gratis primeros usos. Google Cloud: $0-1/mes. Drive: Gratis.
   Si usas PythonAnywhere: $5/mes (opcional).

P: ¿Puedo compartir mi Excel?
R: SÍ en Google Drive. Right-click → Share → Invita gente.

P: ¿Qué pasa si el bot falla?
R: Reinicia: python main.py

═══════════════════════════════════════════════════════════════════════════
✨ ¡LISTO PARA USAR!
═══════════════════════════════════════════════════════════════════════════

Abre Telegram y busca tu bot.
Comienza a registrar gastos.
¡Que disfrutes! 🎉

═══════════════════════════════════════════════════════════════════════════
""")

input("Presiona ENTER para terminar...")
