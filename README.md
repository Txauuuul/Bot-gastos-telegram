# Bot de Telegram para Análisis de Tickets 📸

Bot inteligente que lee fotos de tickets de compra y extrae información de gastos automáticamente. También acepta entrada manual de gastos.

## ✨ Características

- 📸 **OCR de Tickets**: Procesa fotos automáticamente (Google Cloud Vision o Tesseract)
- 💬 **Parser de Texto**: Escribe "Patatas 2.50€" y se registra automáticamente
- 📊 **Excel Automático**: Todos los gastos se guardan en archivo Excel estructurado
- ☁️ **Google Drive**: Sincronización automática (opcional)
- 📈 **Resumen**: Consulta gastos totales, cantidad y promedio

## Estructura del Proyecto

```
Pop/
├── main.py              # Código principal del bot
├── expense_parser.py    # Parser de gastos en texto
├── spreadsheet_manager.py # Gestión de Excel y Google Drive
├── ocr_processor.py     # Procesamiento OCR de imágenes
├── requirements.txt     # Dependencias necesarias
├── .env                 # Variables de entorno (no subir a git)
├── .env.example         # Ejemplo de configuración
├── .gitignore          # Archivos a ignorar en git
└── README.md           # Este archivo
```

## 🚀 Inicio Rápido

### ⭐ OPCIÓN 1: Guía Paso a Paso Completa (RECOMENDADO)

**Si es la PRIMERA VEZ y no sabes qué hacer, ejecuta esto:**

```powershell
python GUIA_PASO_A_PASO.py
```

Te mostrará:
- ✅ Cómo obtener token de Telegram
- ✅ Cómo crear archivo .env
- ✅ Cómo instalar librerías
- ✅ Cómo probar el bot
- ✅ Cómo configurar OCR (opcional)
- ✅ Cómo sincronizar con Google Drive (opcional)

**Tiempo: 15-20 minutos**

### ⭐ OPCIÓN 2: Checklist Rápido

**Si sabes qué haces y quieres solo un checklist visual:**

```powershell
python CHECKLIST_RAPIDO.py
```

Versión abreviada con todos los pasos.

### ⭐ OPCIÓN 3: Manual (Si prefieres leer)

#### 1. Obtener Token de Telegram

1. Abre Telegram y busca a **@BotFather**
2. Escribe `/newbot` y sigue las instrucciones
3. Copia el token que te proporciona

#### 2. Crear archivo .env

1. En VS Code, crea un nuevo archivo: `Ctrl+N`
2. Copia esto (reemplaza el TOKEN):
```
TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI_SIN_COMILLAS
USE_GOOGLE_DRIVE=false
WEBHOOK_URL=
WEBHOOK_PORT=443
WEBHOOK_SECRET=tu_password_secreto
```
3. Guarda como `.env` en `c:\Users\User\Pop`
4. **⚠️ IMPORTANTE:** Este archivo está en `.gitignore`

#### 3. Instalar Dependencias

Abre terminal en VS Code (`Ctrl+``) y ejecuta:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Ejecutar el Bot

```powershell
python main.py
```

Deberías ver:
```
INFO:__main__:🤖 Bot iniciado. Presiona Ctrl+C para detener.
```

#### 5. Prueba

- Abre Telegram y busca tu bot
- Escribe `/start`
- Escribe `Patatas 2.50€`
- Verifica que aparece `gastos.xlsx` en la carpeta

---

## 📱 Cómo Usar el Bot

### Comando /start
Comienza la conversación y obtén bienvenida personalizada.

### Enviar Foto de Ticket
1. Toma foto del ticket
2. Envía al bot
3. El bot extrae automáticamente todos los gastos

```
📸 Ticket recibido. Analizando datos...
✅ Gastos agregados al Excel:
• Patatas: 2.50€
• Leche: 1.20€

💰 Total: 3.70€
```

### Escribir Gastos Manualmente

Acepta varios formatos:
```
Patatas 2.50€
Leche: 1.20€
Agua - 2.30€
3.45€ Manzanas
```

Se guardan automáticamente con fecha y hora.

### Comando /resumen
Ver total de gastos del mes actual:
```
📊 Resumen del Mes

💰 Total gastado: 45.50€
🧾 Cantidad de gastos: 12
📈 Promedio por gasto: 3.79€
```

### Comando /ayuda
Ver todos los comandos disponibles.

---

## 🌐 Modo LOCAL vs NUBE

### 💻 MODO LOCAL (Tu PC)
```powershell
python main.py
```
- Usa polling (pregunta constantemente a Telegram)
- ✅ Perfecto para desarrollo
- ❌ Requiere PC encendido
- ❌ Más lento

### ☁️ MODO NUBE (PythonAnywhere / Heroku)
```
Bot corre en servidor 24/7
```
- Usa webhooks (respuesta instantánea)
- ✅ Funciona sin PC encendido
- ✅ Más rápido
- ✅ Mejor para producción

**La detección es automática:**
- Si `WEBHOOK_URL` en `.env` está lleno → **MODO NUBE**
- Si `WEBHOOK_URL` está vacío → **MODO LOCAL**

---

## 📊 Archivos Generados

### gastos.xlsx
Archivo Excel automático con:
- **Fecha**: Día del gasto
- **Hora**: Hora exacta
- **Concepto**: Qué se compró
- **Precio**: Cantidad en €
- **Categoría**: Ticket o Manual

Estilos profesionales con encabezados coloreados y bordes.

---

## 🌐 Modo LOCAL vs NUBE

### 💻 MODO LOCAL (Tu PC)
```powershell
python main.py
```
- Usa polling (pregunta constantemente a Telegram)
- ✅ Perfecto para desarrollo
- ❌ Requiere PC encendido
- ❌ Más lento

### ☁️ MODO NUBE (PythonAnywhere / Heroku)
```
Bot corre en servidor 24/7
```
- Usa webhooks (respuesta instantánea)
- ✅ Funciona sin PC encendido
- ✅ Más rápido
- ✅ Mejor para producción

**La detección es automática:**
- Si `WEBHOOK_URL` en `.env` está lleno → **MODO NUBE**
- Si `WEBHOOK_URL` está vacío → **MODO LOCAL**

---

## ☁️ Desplegar en PythonAnywhere (RECOMENDADO)

PythonAnywhere permite que tu bot funcione 24/7 sin tu PC encendido.

### Configuración Rápida

1. Abre [PythonAnywhere](https://www.pythonanywhere.com)
2. Crea cuenta gratis
3. Sube tu código
4. Configura `.env` con `WEBHOOK_URL`
5. Ejecuta `python setup_webhook.py`

**Para instrucciones detalladas, abre: [GUIA_PYTHONANYWHERE.py](GUIA_PYTHONANYWHERE.py)**

### Ventajas PythonAnywhere
- ✅ Gratis (plan Beginner)
- ✅ $5/mes para acceso 24/7 (recomendado)
- ✅ Bot funciona aunque PC esté apagado
- ✅ Respuestas instantáneas
- ✅ Sincronización automática con Google Drive

### Costo Total Aproximado
- **PythonAnywhere**: $5/mes (plan Hacker 24/7)
- **Google Cloud Vision**: $0-1/mes (crédito gratis $300)
- **Google Drive**: Gratis (15GB)
- **Total**: ~$5/mes para tener bot funcional 24/7

---

## ☁️ Google Drive (Opcional)

### Activar Sincronización

1. Cambiar en `.env`:
```
USE_GOOGLE_DRIVE=true
```

2. Configurar credenciales:
   - Ir a [Google Cloud Console](https://console.cloud.google.com)
   - Crear proyecto nuevo
   - Habilitar "Google Drive API"
   - Crear "OAuth 2.0 Client ID" (tipo desktop)
   - Descargar JSON como `credentials.json`
   - Guardar `credentials.json` en carpeta del bot

3. Primera ejecución:
   - Se abrirá navegador para autenticar
   - Se genera `token.json` automáticamente
   - Excel se sincroniza cada vez que agregas un gasto

---

## 🤖 OCR - Métodos Disponibles

### Opción 1: Google Cloud Vision (Recomendado)
- ✅ Muy preciso
- ✅ Maneja rotaciones y luz mala
- ✅ Crédito gratis $300 de Google
- ❌ Requiere API key

```powershell
pip install google-cloud-vision
```

### Opción 2: Tesseract (Local, Gratis)
- ✅ Nunca requiere internet
- ✅ Totalmente gratis
- ❌ Menos preciso que Vision
- ❌ Lento en máquinas antiguas

En Windows:
1. Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar en `C:\Program Files\Tesseract-OCR`
3. Instalar librerías:
```powershell
pip install pytesseract pillow
```

### Opción 3: Solo Texto Manual (Gratis, Sin OCR)
- ✅ Sin dependencias
- ✅ Muy rápido
- ✅ Perfecto para empezar
- ❌ No procesa fotos automáticamente

Esta es la opción por defecto. Luego puedes agregar OCR.

---

## 🔧 Solución de Problemas

### Error: "TELEGRAM_BOT_TOKEN no encontrado"
**Solución**: Asegúrate de que el archivo `.env` existe con el token correcto.

### Error: "ModuleNotFoundError"
**Solución**: Ejecuta `pip install -r requirements.txt`

### El bot no responde a fotos
**Solución**: 
- Sin OCR configurado es normal (solo acepta texto)
- Para OCR: instala Google Cloud Vision o Tesseract
- Reinicia el bot después

### Google Drive no funciona
**Solución**:
- Verifica que `credentials.json` existe
- Comprueba que Google Drive API esté habilitada
- Elimina `token.json` y reinicia para reauthenticar

---

## 📦 Versiones Requeridas

- Python 3.8+
- `python-telegram-bot >= 20.0` (con asyncio)
- `openpyxl >= 3.0` (Excel)
- `python-dotenv >= 1.0` (variables de entorno)
- `google-api-python-client` (si usas Google Drive)

---

## 🚀 Próximas Mejoras

- [ ] Categorización automática de gastos
- [ ] Gráficos mensuales y anuales
- [ ] Búsqueda de gastos por fecha
- [ ] Exportar a PDF
- [ ] Base de datos en lugar de Excel
- [ ] Compartir gastos con otros usuarios

---

**Creado**: Febrero 2026  
**Última actualización**: Febrero 2026  
**Licencia**: MIT
