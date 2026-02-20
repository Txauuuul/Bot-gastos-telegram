"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                   📚 ÍNDICE DE DOCUMENTACIÓN DEL BOT                      ║
║                                                                            ║
║              ¿POR DÓNDE EMPIEZO? LEE ESTO PRIMERO                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

print(__doc__)

menu = """

═══════════════════════════════════════════════════════════════════════════
🤔 ELIGE TU SITUACIÓN:
═══════════════════════════════════════════════════════════════════════════

1️⃣  "NUNCA HE HECHO ESTO Y NO SÉ CÓMO EMPEZAR"
    └─ 👉 Ejecuta: python GUIA_PASO_A_PASO.py
    └─ ⏱️  Tiempo: 15-20 minutos
    └─ 📝 Incluye: TODO (Token, instalación, configuración, pruebas)
    └─ 🎯 Mejor para: Principiantes totales

2️⃣  "SAÉ BÁSICAMENTE QUÉ HACER PERO QUIERO UN CHECKLIST"
    └─ 👉 Ejecuta: python CHECKLIST_RAPIDO.py
    └─ ⏱️  Tiempo: 10 minutos
    └─ 📝 Incluye: Checklist resumido de todos los pasos
    └─ 🎯 Mejor para: Usuarios con experiencia

3️⃣  "QUIERO LEER DOCUMENTACIÓN DETALLADA"
    └─ 👉 Lee: README.md
    └─ ⏱️  Tiempo: 10-15 minutos
    └─ 📝 Incluye: Características, comandos, troubleshooting
    └─ 🎯 Mejor para: Referencia general

4️⃣  "YA FUNCIONÓ EN LOCAL, QUIERO PASAR A NUBE (PythonAnywhere)"
    └─ 👉 Lee: GUIA_PYTHONANYWHERE.py
    └─ ⏱️  Tiempo: 20-30 minutos
    └─ 📝 Incluye: Configuración en servidor 24/7
    └─ 🎯 Mejor para: Pasar de desarrollo a producción

5️⃣  "QUIERO CONFIGURAR OCR (LEER FOTOS) Y GOOGLE DRIVE"
    └─ 👉 Lee: SETUP_INTEGRACIONES.py
    └─ ⏱️  Tiempo: 10-15 minutos
    └─ 📝 Incluye: Google Cloud Vision, Tesseract, Google Drive
    └─ 🎯 Mejor para: Agregar funcionalidades avanzadas

6️⃣  "TENGO UN PROBLEMA Y NECESITO AYUDA"
    └─ 👉 Ve a → README.md → Sección "Solución de Problemas"
    └─ ⏱️  Tiempo: 2-5 minutos
    └─ 📝 Incluye: Errores comunes y cómo resolverlos
    └─ 🎯 Mejor para: Debugging rápido

═══════════════════════════════════════════════════════════════════════════
📊 FLUJO RECOMENDADO:
═══════════════════════════════════════════════════════════════════════════

SEMANA 1 - Setup Inicial:
  1️⃣ GUIA_PASO_A_PASO.py      (15-20 min)
  2️⃣ python main.py            (instancia local)
  3️⃣ Prueba escribiendo gastos


SEMANA 2 - Mejorar:
  4️⃣ SETUP_INTEGRACIONES.py    (15 min)
  5️⃣ Configura OCR (Vision o Tesseract)
  6️⃣ Configura Google Drive
  7️⃣ Prueba enviando fotos


SEMANA 3 - Producción:
  8️⃣ GUIA_PYTHONANYWHERE.py    (20-30 min)
  9️⃣ Sube a servidor en la nube
     Bot corre 24/7 sin tu PC


═══════════════════════════════════════════════════════════════════════════
📁 ARCHIVOS DISPONIBLES:
═══════════════════════════════════════════════════════════════════════════

GUÍAS (Ejecutables):
  → python GUIA_PASO_A_PASO.py       Guía interactiva completa ⭐
  → python CHECKLIST_RAPIDO.py       Checklist visual rápido ⭐
  → python SETUP_INTEGRACIONES.py    OCR y Google Drive
  → python GUIA_PYTHONANYWHERE.py    Desplegar en servidor

DOCUMENTACIÓN (Para leer):
  → README.md                        Documentación general
  → este archivo                     (índice)

CÓDIGO DEL BOT (No editar):
  → main.py                          Bot principal
  → expense_parser.py                Parser de gastos
  → spreadsheet_manager.py           Gestor de Excel/Drive
  → ocr_processor.py                 OCR de imágenes
  → pythonanywhere_wsgi.py          Para servidor nube

CONFIGURACIÓN:
  → .env                             Tu configuración secreta (creas tú)
  → .env.example                     Plantilla de .env
  → requirements.txt                 Librerías a instalar

EJECUCIÓN RÁPIDA:
  → instalar.bat                     Instala todo automáticamente
  → ejecutar.bat                     Lanza el bot rápidamente

═══════════════════════════════════════════════════════════════════════════
🎯 RECOMENDACIÓN PARA TI:
═══════════════════════════════════════════════════════════════════════════

Si es tu PRIMERA VEZ:
  ╔═════════════════════════════════════════════════════════════════════╗
  ║  Ejecuta esto en la terminal de VS Code:                          ║
  ║  python GUIA_PASO_A_PASO.py                                       ║
  ║                                                                    ║
  ║  Te guiará paso a paso por toda la instalación.                  ║
  ╚═════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
⚡ ACCESO DIRECTO (COPIAR Y PEGAR):
═══════════════════════════════════════════════════════════════════════════

OPCIÓN 1: Guía interactiva completa
  python GUIA_PASO_A_PASO.py

OPCIÓN 2: Checklist rápido visual
  python CHECKLIST_RAPIDO.py

OPCIÓN 3: Ejecutar el bot directamente
  python main.py

═══════════════════════════════════════════════════════════════════════════
💡 TIPS:
═══════════════════════════════════════════════════════════════════════════

• Si algo falla, lee el mensaje de error en la terminal
• Todos los archivos .py se pueden ejecutar con: python nombre.py
• .env es tu archivo secreto, NO lo compartas
• Excel (gastos.xlsx) se crea automáticamente
• Cualquier duda, pregúntame con el error específico

═══════════════════════════════════════════════════════════════════════════
🚀 ¡VAMOS A EMPEZAR!
═══════════════════════════════════════════════════════════════════════════

Abre una terminal en VS Code (Ctrl+`)
Copia una de estas opciones:

  python GUIA_PASO_A_PASO.py        ← RECOMENDADO PARA PRINCIPIANTES
  python CHECKLIST_RAPIDO.py        ← SI YA SABES QUÉ HACER

Presiona Enter y sigue las instrucciones.

═══════════════════════════════════════════════════════════════════════════
"""

print(menu)
