"""
Bot de Telegram para gestión avanzada de gastos.
Utiliza python-telegram-bot v20+ con asyncio.
Compatible con LOCAL (polling) y NUBE (webhooks).
"""

import logging
import os
import tempfile
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from expense_parser import ExpenseParser
from spreadsheet_manager import SpreadsheetManager
from ocr_processor import procesar_ticket, parseador_ticket

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Diccionario para almacenar gastos pendientes
gastos_pendientes = {}

# Configuración
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USE_GOOGLE_DRIVE = os.getenv("USE_GOOGLE_DRIVE", "false").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "tu_secret")

MODE_NUBE = WEBHOOK_URL is not None

if not TOKEN:
    raise ValueError(
        "⚠️  Error: TELEGRAM_BOT_TOKEN no encontrado en archivo .env\n"
        "Asegúrate de crear un archivo .env con tu token."
    )

spreadsheet = SpreadsheetManager(use_google_drive=USE_GOOGLE_DRIVE)

logger.info(f"🌐 Modo: {'NUBE (webhooks)' if MODE_NUBE else 'LOCAL (polling)'}")


# ============================================================================
# COMANDOS BÁSICOS
# ============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start - Bienvenida."""
    user_name = update.effective_user.first_name
    welcome_message = (
        f"¡Hola {user_name}! 👋\n\n"
        "Bienvenido a tu bot de contabilidad de gastos.\n\n"
        "📸 *Cosas que puedo hacer:*\n"
        "• Recibir fotos de tickets → OCR automático\n"
        "• Analizar gastos → Guardar en Excel\n"
        "• Parser de texto → 'Patatas 2.50€' o 'Patatas 2'\n\n"
        "📝 *Cómo usarme:*\n"
        "1️⃣ Envía una foto de un ticket y analizaré los gastos\n"
        "2️⃣ O escribe gastos como: 'Patatas 2.50€' o 'Leche 1'\n"
        "3️⃣ Selecciona la categoría\n"
        "4️⃣ Usa /ayuda para ver todos los comandos\n\n"
        "📊 Excel: Se guarda automáticamente en gastos.xlsx"
        f"{' ☁️ y se sincroniza con Google Drive' if USE_GOOGLE_DRIVE else ''}"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")
    logger.info(f"Usuario {user_name} (ID: {update.effective_user.id}) ejecutó /start")


async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ayuda - Muestra todos los comandos disponibles."""
    ayuda = (
        "🆘 *COMANDOS DISPONIBLES*\n\n"
        "*📊 BÁSICOS:*\n"
        "/start - Información inicial\n"
        "/resumen - Gastos del mes actual\n"
        "/ultimos <días> - Gastos de los últimos X días\n"
        "/estado - Gasto total de hoy\n\n"
        "*📈 ANÁLISIS Y REPORTES:*\n"
        "/estadisticas - Gasto por categoría (gráfico)\n"
        "/categoria <nombre> - Total de una categoría\n"
        "/promedio - Promedio diario de gasto\n"
        "/comparar - Mes actual vs mes anterior\n"
        "/proyeccion - Predicción de gasto del mes\n"
        "/ahorro - Opciones para ahorrar por categoría\n"
        "/ranking - Gastos más frecuentes\n"
        "/top - Top 5 gastos más caros\n\n"
        "*🔍 BÚSQUEDA Y FILTRADO:*\n"
        "/buscar <palabra> - Buscar por concepto\n"
        "/entre <fecha1> <fecha2> - Rango de fechas (DD/MM/YYYY)\n"
        "/mes <número> - Gastos de un mes específico\n"
        "/historial - Últimos 5 gastos\n\n"
        "*✂️ GESTIÓN DE GASTOS:*\n"
        "/borrar <concepto> - Elimina el último gasto\n"
        "/deshacer - Restaura el último gasto borrado\n"
        "/editar <concepto> <nuevo_precio> - Modifica precio\n"
        "/duplicar <concepto> - Registra el gasto nuevamente\n\n"
        "*🏷️ CATEGORÍAS PERSONALIZADAS:*\n"
        "/categorias - Lista de categorías\n"
        "/agregar_cat <nombre> - Nueva categoría\n"
        "/eliminar_cat <nombre> - Elimina categoría\n\n"
        "*💰 PRESUPUESTO:*\n"
        "/presupuesto - Ver límites actuales\n"
        "/establecer_presupuesto <diario> <mensual> - Configurar límites\n\n"
        "*Ejemplos:*\n"
        "Patatas 2.50€\n"
        "/ultimos 7\n"
        "/buscar leche\n"
        "/entre 01/02/2026 15/02/2026\n"
        "/editar patatas 3.50\n"
        "/duplicar café"
    )
    await update.message.reply_text(ayuda, parse_mode="Markdown")


# ============================================================================
# MANEJADOR DE FOTOS Y TEXTO
# ============================================================================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para fotos de tickets."""
    user_id = update.effective_user.id

    try:
        await update.message.reply_text("📸 Ticket recibido. Analizando datos...")

        photo_file = await update.message.photo[-1].get_file()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            imagen_path = os.path.join(tmpdir, "ticket.jpg")
            await photo_file.download_to_drive(imagen_path)

            logger.info(f"Usuario {user_id} envió un ticket. Procesando OCR...")
            resultado_ocr = await procesar_ticket(imagen_path)

            if not resultado_ocr:
                await update.message.reply_text(
                    "❌ No pude extraer el texto del ticket.\n"
                    "Intenta con una foto más clara o escribe manualmente:\n"
                    "Ejemplo: 'Patatas 2.50€'"
                )
                return

            texto = resultado_ocr.get("texto", "")
            metodo = resultado_ocr.get("metodo", "desconocido")
            lineas = parseador_ticket(texto)

            if not lineas:
                await update.message.reply_text(
                    f"📄 Ticket analizado (método: {metodo})\n\n"
                    "⚠️ No encontré líneas de compra con formato claro.\n\n"
                    "Texto extraído:\n"
                    f"<code>{texto[:500]}</code>\n\n"
                    "Puedes escribir manualmente: 'Patatas 2.50€'"
                )
                return

            total = 0
            mensaje_resumen = "✅ Gastos agregados al Excel:\n\n"

            fecha = datetime.now().strftime("%d/%m/%Y")
            hora = datetime.now().strftime("%H:%M:%S")

            for linea in lineas:
                try:
                    precio = float(linea["precio"].replace(",", "."))
                    total += precio

                    gasto = {
                        "concepto": linea["concepto"],
                        "precio": precio,
                        "fecha": fecha,
                        "hora": hora,
                        "categoria": "Ticket",
                    }

                    if spreadsheet.agregar_gasto(gasto):
                        mensaje_resumen += f"• {linea['concepto']}: {precio:.2f}€\n"
                except ValueError:
                    logger.warning(f"No se pudo procesar línea: {linea}")

            mensaje_resumen += f"\n💰 Total: {total:.2f}€\n"
            mensaje_resumen += f"📊 Método OCR: {metodo}"

            await update.message.reply_text(mensaje_resumen)
            resumen = spreadsheet.obtener_resumen()
            
            if resumen["cantidad"] > 0:
                await update.message.reply_text(
                    f"📈 Mes actual:\n"
                    f"• Gastos: {resumen['cantidad']}\n"
                    f"• Total: {resumen['total']:.2f}€\n"
                    f"• Promedio: {resumen['promedio']:.2f}€"
                )

    except Exception as e:
        logger.error(f"Error procesando ticket: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n"
            "Intenta de nuevo o escribe manualmente: 'Patatas 2.50€'"
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para parsear gastos de texto."""
    user_id = update.effective_user.id
    texto = update.message.text.strip()

    if texto.startswith("/"):
        return

    gasto_parsed = ExpenseParser.parse(texto)
    es_válido, mensaje_validacion = ExpenseParser.validar_gasto(gasto_parsed)

    if not es_válido:
        await update.message.reply_text(mensaje_validacion)
        return

    gastos_pendientes[user_id] = gasto_parsed

    categorias = spreadsheet.obtener_categorias()
    buttons = []
    
    for categoria in categorias:
        buttons.append([InlineKeyboardButton(categoria, callback_data=f"cat_{categoria}")])

    keyboard = InlineKeyboardMarkup(buttons)

    mensaje = (
        f"✅ Gasto parseado:\n"
        f"• Concepto: {gasto_parsed['concepto']}\n"
        f"• Precio: {gasto_parsed['precio']:.2f}€\n\n"
        f"🏷️  ¿En qué categoría lo registramos?"
    )

    await update.message.reply_text(mensaje, reply_markup=keyboard)
    logger.info(
        f"Usuario {user_id} parseó gasto: {gasto_parsed['concepto']} - {gasto_parsed['precio']}€"
    )


async def categoria_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador de callback para categorías."""
    query = update.callback_query
    user_id = query.from_user.id
    
    categoria_seleccionada = query.data.replace("cat_", "")
    
    if user_id not in gastos_pendientes:
        await query.answer("❌ No hay gasto pendiente. Intenta de nuevo.", show_alert=True)
        return
    
    gasto_parsed = gastos_pendientes[user_id]
    gasto_parsed["categoria"] = categoria_seleccionada
    
    if spreadsheet.agregar_gasto(gasto_parsed):
        respuesta = (
            f"✅ Gasto registrado:\n"
            f"• Concepto: {gasto_parsed['concepto']}\n"
            f"• Precio: {gasto_parsed['precio']:.2f}€\n"
            f"• Categoría: {categoria_seleccionada}\n"
            f"• Fecha: {gasto_parsed['fecha']} {gasto_parsed['hora']}"
        )
        
        await query.edit_message_text(text=respuesta)
        del gastos_pendientes[user_id]
        
        logger.info(
            f"Usuario {user_id} confirmó gasto: {gasto_parsed['concepto']} - {gasto_parsed['precio']}€ "
            f"en categoría {categoria_seleccionada}"
        )
    else:
        await query.answer("❌ Error al guardar el gasto. Intenta de nuevo.", show_alert=True)
    
    await query.answer()


# ============================================================================
# COMANDOS - RESUMEN Y ESTADO
# ============================================================================

async def resumen_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /resumen - Resumen del mes actual."""
    resumen = spreadsheet.obtener_resumen()

    mensaje = (
        "📊 *Resumen del Mes*\n\n"
        f"💰 Total gastado: {resumen['total']:.2f}€\n"
        f"🧾 Cantidad de gastos: {resumen['cantidad']}\n"
        f"📈 Promedio por gasto: {resumen['promedio']:.2f}€"
    )

    await update.message.reply_text(mensaje, parse_mode="Markdown")
    logger.info(f"Usuario {update.effective_user.id} consultó resumen")


async def estado_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /estado - ¿Cuánto he gastado hoy?"""
    hoy = datetime.now().strftime("%d/%m/%Y")
    resultado = spreadsheet.obtener_gasto_del_dia(hoy)
    
    if resultado["total"] == 0:
        await update.message.reply_text(f"✨ ¡Aún no has gastado nada hoy! 💪")
        return
    
    mensaje = f"📊 *Gasto de hoy ({hoy}):*\n\n"
    
    for gasto in resultado["gastos"]:
        mensaje += f"• {gasto['concepto']}: {gasto['precio']:.2f}€ ({gasto['categoria']})\n"
    
    mensaje += f"\n💰 *Total hoy: {resultado['total']:.2f}€*"
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")


async def ultimos_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ultimos - Gastos de los últimos X días."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: /ultimos <días>\n\n"
            "Ejemplos:\n"
            "/ultimos 7  → Últimos 7 días\n"
            "/ultimos 30 → Últimos 30 días\n"
            "/ultimos 1  → Hoy"
        )
        return
    
    try:
        dias = int(context.args[0])
        
        if dias <= 0:
            await update.message.reply_text("❌ El número de días debe ser mayor a 0")
            return
        
        resultado = spreadsheet.obtener_gastos_ultimos_dias(dias)
        
        if resultado["cantidad"] == 0:
            await update.message.reply_text(
                f"📭 No hay gastos registrados en los últimos {dias} días"
            )
            return
        
        mensaje = f"📊 *Gastos de los últimos {dias} día(s):*\n\n"
        
        for gasto in resultado["gastos"]:
            mensaje += (
                f"📅 {gasto['fecha']} | ⏰ {gasto['hora']}\n"
                f"   {gasto['concepto']}: *{gasto['precio']:.2f}€*\n"
                f"   🏷️  {gasto['categoria']}\n\n"
            )
        
        mensaje += (
            f"─────────────────────────\n"
            f"💰 *Total:* {resultado['total']:.2f}€\n"
            f"🧾 *Gastos:* {resultado['cantidad']}"
        )
        
        await update.message.reply_text(mensaje, parse_mode="Markdown")
        logger.info(f"Usuario {user_id} consultó gastos de últimos {dias} días")
    
    except ValueError:
        await update.message.reply_text(
            "❌ Debes ingresar un número válido\n\n"
            "Ejemplo: /ultimos 7"
        )


# ============================================================================
# COMANDOS - ANÁLISIS Y ESTADÍSTICAS
# ============================================================================

async def estadisticas_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /estadisticas - Gasto por categoría con gráfico ASCII."""
    categorias = spreadsheet.obtener_gastos_por_categoria()
    
    if not categorias:
        await update.message.reply_text("📭 No hay gastos registrados este mes")
        return
    
    total_mes = sum(categorias.values())
    max_valor = max(categorias.values())
    
    mensaje = "📊 *Estadísticas del Mes por Categoría*\n\n"
    
    for categoria, total in categorias.items():
        porcentaje = (total / total_mes) * 100 if total_mes > 0 else 0
        barla_length = int((total / max_valor) * 20) if max_valor > 0 else 0
        barra = "█" * barla_length + "░" * (20 - barla_length)
        
        mensaje += f"{categoria}:\n"
        mensaje += f"[{barra}] {total:.2f}€ ({porcentaje:.1f}%)\n\n"
    
    mensaje += f"*Total: {total_mes:.2f}€*"
    
    await update.message.reply_text(mensaje, parse_mode="Markdown")


async def categoria_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /categoria - Total de una categoría específica."""
    if not context.args:
        categorias = spreadsheet.obtener_categorias()
        msg = "📝 Uso: /categoria <nombre>\n\nCategorías disponibles:\n"
        for cat in categorias:
            msg += f"• {cat}\n"
        await update.message.reply_text(msg)
        return
    
    categoria_buscada = " ".join(context.args)
    categorias = spreadsheet.obtener_gastos_por_categoria()
    
    for cat, total in categorias.items():
        if cat.lower() == categoria_buscada.lower():
            resumen = spreadsheet.obtener_resumen()
            porcentaje = (total / resumen['total'] * 100) if resumen['total'] > 0 else 0
            
            msg = f"🏷️  *{cat}*\n\n"
            msg += f"💰 Total: {total:.2f}€\n"
            msg += f"📊 Porcentaje: {porcentaje:.1f}%\n"
            msg += f"📈 Del total del mes: {total}/{resumen['total']:.2f}€"
            
            await update.message.reply_text(msg, parse_mode="Markdown")
            return
    
    await update.message.reply_text(f"❌ Categoría '{categoria_buscada}' no encontrada")


async def promedio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /promedio - Promedio diario de gasto."""
    promedio = spreadsheet.obtener_promedio_diario()
    resumen = spreadsheet.obtener_resumen()
    
    msg = "📈 *Promedio de Gasto Diario*\n\n"
    msg += f"💰 Promedio: {promedio:.2f}€/día\n"
    msg += f"📊 Mes actual: {resumen['total']:.2f}€ en {resumen['cantidad']} gastos\n"
    msg += f"🧮 Días con gastos: {resumen['cantidad']}"
    
    if promedio > 0:
        msg += f"\n⏰ A este ritmo, gastarías {promedio * 30:.2f}€ en 30 días"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def comparar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /comparar - Comparar mes actual vs mes anterior."""
    hoy = datetime.now()
    mes_actual = hoy.month
    año_actual = hoy.year
    
    if mes_actual == 1:
        mes_anterior = 12
        año_anterior = año_actual - 1
    else:
        mes_anterior = mes_actual - 1
        año_anterior = año_actual
    
    gastos_actual = spreadsheet.obtener_gastos_por_mes(mes_actual, año_actual)
    gastos_anterior = spreadsheet.obtener_gastos_por_mes(mes_anterior, año_anterior)
    
    diferencia = gastos_actual["total"] - gastos_anterior["total"]
    porcentaje = (diferencia / gastos_anterior["total"] * 100) if gastos_anterior["total"] > 0 else 0
    
    simbolo = "📈" if diferencia > 0 else "📉" if diferencia < 0 else "➡️"
    
    msg = f"📊 *Comparación de Meses*\n\n"
    msg += f"Mes actual: {gastos_actual['total']:.2f}€ ({gastos_actual['cantidad']} gastos)\n"
    msg += f"Mes anterior: {gastos_anterior['total']:.2f}€ ({gastos_anterior['cantidad']} gastos)\n\n"
    msg += f"{simbolo} Diferencia: {abs(diferencia):.2f}€ ({porcentaje:+.1f}%)"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def proyeccion_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /proyeccion - Predicción de gasto del mes."""
    proyeccion = spreadsheet.obtener_proyeccion_mes()
    
    if "error" in proyeccion:
        await update.message.reply_text(f"❌ {proyeccion['error']}")
        return
    
    msg = "🔮 *Proyección del Mes*\n\n"
    msg += f"📊 Gasto actual: {proyeccion['gasto_actual']:.2f}€\n"
    msg += f"⏰ Días transcurridos: {proyeccion['dias_transcurridos']}\n"
    msg += f"📈 Promedio diario: {proyeccion['promedio_diario']:.2f}€\n"
    msg += f"🎯 Proyección mes: {proyeccion['proyeccion_mes']:.2f}€\n"
    msg += f"💾 Presupuesto: {proyeccion['diferencia_presupuesto']:.2f}€"
    
    if proyeccion['diferencia_presupuesto'] > 0:
        msg += " ✅ (Dentro de presupuesto)"
    else:
        msg += " ⚠️ (Excede presupuesto)"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def ahorro_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ahorro - Opciones para ahorrar."""
    ahorro = spreadsheet.obtener_ahorro_potencial()
    
    if not ahorro:
        await update.message.reply_text("📭 No hay gastos registrados")
        return
    
    msg = "💰 *Opciones de Ahorro Por Categoría*\n\n"
    
    for categoria, opciones in ahorro.items():
        msg += f"*{categoria}:* {opciones['gasto_actual']:.2f}€\n"
        msg += f"  • Reducir 10%: Ahorrarías {opciones['reducir_10%']:.2f}€\n"
        msg += f"  • Reducir 25%: Ahorrarías {opciones['reducir_25%']:.2f}€\n"
        msg += f"  • Reducir 50%: Ahorrarías {opciones['reducir_50%']:.2f}€\n\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def ranking_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ranking - Gastos más frecuentes."""
    ranking = spreadsheet.obtener_ranking_gastos()
    
    if not ranking:
        await update.message.reply_text("📭 No hay gastos registrados")
        return
    
    msg = "🏆 *Ranking de Gastos Más Frecuentes*\n\n"
    
    for i, (concepto, datos) in enumerate(ranking.items(), 1):
        msg += f"{i}. *{concepto}*\n"
        msg += f"   Total: {datos['total']:.2f}€ ({datos['cantidad']} veces)\n"
        msg += f"   Promedio: {datos['promedio']:.2f}€/vez\n\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /top - Top 5 gastos más caros."""
    top = spreadsheet.obtener_top_gastos(5)
    
    if not top:
        await update.message.reply_text("📭 No hay gastos registrados")
        return
    
    msg = "🔥 *Top 5 Gastos Más Caros*\n\n"
    
    for i, gasto in enumerate(top, 1):
        msg += f"{i}. {gasto['concepto']}: {gasto['precio']:.2f}€\n"
        msg += f"   📅 {gasto['fecha']} | {gasto['categoria']}\n\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


# ============================================================================
# COMANDOS - BÚSQUEDA Y FILTRADO
# ============================================================================

async def buscar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /buscar - Buscar por concepto."""
    if not context.args:
        await update.message.reply_text("❌ Uso: /buscar <palabra clave>\n\nEjemplo: /buscar leche")
        return
    
    palabra = " ".join(context.args)
    resultado = spreadsheet.buscar_por_concepto(palabra)
    
    if resultado["cantidad"] == 0:
        await update.message.reply_text(f"📭 No encontré gastos con '{palabra}'")
        return
    
    msg = f"🔍 *Resultados para '{palabra}':*\n\n"
    
    for gasto in resultado["gastos"][:10]:
        msg += f"• {gasto['concepto']}: {gasto['precio']:.2f}€\n"
        msg += f"  📅 {gasto['fecha']} | {gasto['categoria']}\n\n"
    
    msg += f"📊 Total encontrado: {resultado['total']:.2f}€ ({resultado['cantidad']} gastos)"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def entre_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /entre - Gastos entre dos fechas."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Uso: /entre <fecha_inicio> <fecha_fin>\n\n"
            "Formato: DD/MM/YYYY\n"
            "Ejemplo: /entre 01/02/2026 15/02/2026"
        )
        return
    
    try:
        fecha_inicio = context.args[0]
        fecha_fin = context.args[1]
        
        resultado = spreadsheet.obtener_gastos_entre_fechas(fecha_inicio, fecha_fin)
        
        if "error" in resultado:
            await update.message.reply_text(f"❌ {resultado['error']}")
            return
        
        if resultado["cantidad"] == 0:
            await update.message.reply_text(f"📭 No hay gastos en ese período")
            return
        
        msg = f"📅 *Gastos de {resultado['periodo']}:*\n\n"
        
        for gasto in resultado["gastos"][:15]:
            msg += f"• {gasto['concepto']}: {gasto['precio']:.2f}€\n"
            msg += f"  {gasto['fecha']} | {gasto['categoria']}\n\n"
        
        msg += f"💰 Total: {resultado['total']:.2f}€ ({resultado['cantidad']} gastos)"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error en /entre: {e}")
        await update.message.reply_text("❌ Error al procesar el comando")


async def mes_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /mes - Gastos de un mes específico."""
    if not context.args:
        await update.message.reply_text("❌ Uso: /mes <número>\n\nEjemplo: /mes 2 (para febrero)")
        return
    
    try:
        mes = int(context.args[0])
        
        if mes < 1 or mes > 12:
            await update.message.reply_text("❌ El mes debe ser entre 1 y 12")
            return
        
        año = int(context.args[1]) if len(context.args) > 1 else datetime.now().year
        resultado = spreadsheet.obtener_gastos_por_mes(mes, año)
        
        if resultado["cantidad"] == 0:
            await update.message.reply_text(f"📭 No hay gastos registrados en ese mes")
            return
        
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        msg = f"📊 *Gastos de {meses[mes]} de {año}:*\n\n"
        
        for gasto in resultado["gastos"][:15]:
            msg += f"• {gasto['concepto']}: {gasto['precio']:.2f}€\n"
            msg += f"  {gasto['fecha']} | {gasto['categoria']}\n\n"
        
        msg += f"💰 Total: {resultado['total']:.2f}€\n"
        msg += f"📈 Gastos: {resultado['cantidad']}"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Ingresa un número válido\n\nEjemplo: /mes 2")


async def historial_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /historial - Últimos 5 gastos."""
    historial = spreadsheet.obtener_historial_gastos(5)
    
    if not historial:
        await update.message.reply_text("📭 No hay gastos registrados")
        return
    
    msg = "📜 *Últimos 5 Gastos Registrados:*\n\n"
    
    for gasto in historial:
        msg += f"• {gasto['concepto']}: {gasto['precio']:.2f}€\n"
        msg += f"  {gasto['fecha']} {gasto['hora']} | {gasto['categoria']}\n\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


# ============================================================================
# COMANDOS - GESTIÓN DE GASTOS
# ============================================================================

async def borrar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /borrar - Elimina un gasto."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: /borrar <concepto>\n\n"
            "Ejemplo: /borrar patatas"
        )
        return
    
    concepto = " ".join(context.args)
    resultado = spreadsheet.eliminar_gasto(concepto)
    
    await update.message.reply_text(resultado["mensaje"])
    
    if resultado["exito"]:
        logger.info(f"Usuario {user_id} eliminó gasto: {resultado['concepto']}")
    else:
        logger.warning(f"Usuario {user_id} intentó eliminar '{concepto}' pero no se encontró")


async def deshacer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /deshacer - Restaura el último gasto borrado."""
    resultado = spreadsheet.deshacer_ultimo_gasto()
    await update.message.reply_text(resultado["mensaje"])


async def editar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /editar - Modifica el precio de un gasto."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Uso: /editar <concepto> <nuevo_precio>\n\n"
            "Ejemplo: /editar patatas 3.50"
        )
        return
    
    concepto = context.args[0]
    
    try:
        nuevo_precio = float(context.args[1].replace(",", "."))
        resultado = spreadsheet.editargasto(concepto, nuevo_precio=nuevo_precio)
        await update.message.reply_text(resultado["mensaje"])
    except ValueError:
        await update.message.reply_text("❌ El precio debe ser un número válido")


async def duplicar_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /duplicar - Registra el mismo gasto nuevamente."""
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: /duplicar <concepto>\n\n"
            "Ejemplo: /duplicar café"
        )
        return
    
    concepto = " ".join(context.args)
    resultado = spreadsheet.duplicar_gasto(concepto)
    await update.message.reply_text(resultado["mensaje"])


# ============================================================================
# COMANDOS - CATEGORÍAS
# ============================================================================

async def categorias_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /categorias - Lista de categorías."""
    categorias = spreadsheet.obtener_categorias()
    
    msg = "🏷️  *Categorías Disponibles:*\n\n"
    for cat in categorias:
        msg += f"• {cat}\n"
    
    msg += "\n💡 Puedes agregar más con /agregar_cat <nombre>"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def agregar_cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /agregar_cat - Agrega una categoría."""
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: /agregar_cat <nombre>\n\n"
            "Ejemplo: /agregar_cat Ropa"
        )
        return
    
    categoria = " ".join(context.args)
    resultado = spreadsheet.agregar_categoria(categoria)
    await update.message.reply_text(resultado["mensaje"])


async def eliminar_cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /eliminar_cat - Elimina una categoría."""
    if not context.args:
        await update.message.reply_text(
            "❌ Uso: /eliminar_cat <nombre>\n\n"
            "Ejemplo: /eliminar_cat Ropa"
        )
        return
    
    categoria = " ".join(context.args)
    resultado = spreadsheet.eliminar_categoria(categoria)
    await update.message.reply_text(resultado["mensaje"])


# ============================================================================
# COMANDOS - PRESUPUESTO
# ============================================================================

async def presupuesto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /presupuesto - Ver límites actuales."""
    config = spreadsheet.obtener_configuracion()
    
    msg = "💰 *Presupuesto Configurado:*\n\n"
    msg += f"📅 Presupuesto Diario: {config.get('presupuesto_diario', 100)}€\n"
    msg += f"📆 Presupuesto Mensual: {config.get('presupuesto_mensual', 3000)}€\n\n"
    msg += "Para cambiar presupuestos usa:\n"
    msg += "/establecer_presupuesto <diario> <mensual>\n\n"
    msg += "Ejemplo: /establecer_presupuesto 50 2000"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


async def establecer_presupuesto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /establecer_presupuesto - Configurar límites."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Uso: /establecer_presupuesto <diario> <mensual>\n\n"
            "Ejemplo: /establecer_presupuesto 50 2000"
        )
        return
    
    try:
        diario = float(context.args[0].replace(",", "."))
        mensual = float(context.args[1].replace(",", "."))
        
        resultado = spreadsheet.establecer_presupuesto(diario, mensual)
        
        if resultado["exito"]:
            msg = f"✅ Presupuesto actualizado:\n\n"
            msg += f"📅 Diario: {resultado['presupuesto_diario']}€\n"
            msg += f"📆 Mensual: {resultado['presupuesto_mensual']}€"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(resultado["mensaje"])
    except ValueError:
        await update.message.reply_text("❌ Los montos deben ser números válidos")


# ============================================================================
# MANEJADOR DE ERRORES
# ============================================================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador de errores."""
    logger.warning(f"Error: {context.error}")
    if update:
        await update.message.reply_text(
            "❌ Disculpa, ocurrió un error procesando tu solicitud.\n"
            "Por favor, intenta de nuevo."
        )


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ayuda", ayuda_command))
    application.add_handler(CommandHandler("resumen", resumen_command))
    application.add_handler(CommandHandler("estado", estado_command))
    application.add_handler(CommandHandler("ultimos", ultimos_command))
    
    # Análisis
    application.add_handler(CommandHandler("estadisticas", estadisticas_command))
    application.add_handler(CommandHandler("categoria", categoria_command))
    application.add_handler(CommandHandler("promedio", promedio_command))
    application.add_handler(CommandHandler("comparar", comparar_command))
    application.add_handler(CommandHandler("proyeccion", proyeccion_command))
    application.add_handler(CommandHandler("ahorro", ahorro_command))
    application.add_handler(CommandHandler("ranking", ranking_command))
    application.add_handler(CommandHandler("top", top_command))
    
    # Búsqueda y filtrado
    application.add_handler(CommandHandler("buscar", buscar_command))
    application.add_handler(CommandHandler("entre", entre_command))
    application.add_handler(CommandHandler("mes", mes_command))
    application.add_handler(CommandHandler("historial", historial_command))
    
    # Gestión de gastos
    application.add_handler(CommandHandler("borrar", borrar_command))
    application.add_handler(CommandHandler("deshacer", deshacer_command))
    application.add_handler(CommandHandler("editar", editar_command))
    application.add_handler(CommandHandler("duplicar", duplicar_command))
    
    # Categorías
    application.add_handler(CommandHandler("categorias", categorias_command))
    application.add_handler(CommandHandler("agregar_cat", agregar_cat_command))
    application.add_handler(CommandHandler("eliminar_cat", eliminar_cat_command))
    
    # Presupuesto
    application.add_handler(CommandHandler("presupuesto", presupuesto_command))
    application.add_handler(CommandHandler("establecer_presupuesto", establecer_presupuesto_command))
    
    # Callbacks y manejadores
    application.add_handler(CallbackQueryHandler(categoria_callback))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # Manejador de errores
    application.add_error_handler(error_handler)

    # Iniciar
    if MODE_NUBE:
        logger.info("☁️  Iniciando en modo NUBE (webhooks)")
        logger.info(f"📡 Webhook URL: {WEBHOOK_URL}")
        
        application.run_webhook(
            listen="0.0.0.0",
            port=WEBHOOK_PORT,
            url_path=TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
        )
    else:
        logger.info("💻 Iniciando en modo LOCAL (polling)")
        logger.info("🤖 Bot iniciado. Presiona Ctrl+C para detener.")
        logger.info(f"📊 Almacenamiento: Excel local + {'Google Drive ☁️' if USE_GOOGLE_DRIVE else 'Local only'}")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
