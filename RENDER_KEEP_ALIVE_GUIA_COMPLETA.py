"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          🔧 KEEP-ALIVE PARA RENDER: GUÍA COMPLETA Y DETALLADA 🔧         ║
║                                                                            ║
║     Cómo evitar que Render pause tu app (Gratuito y sin complicaciones)   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

print(__doc__)

print("""

═══════════════════════════════════════════════════════════════════════════
❓ ¿POR QUÉ RENDER PAUSA LAS APPS?
═══════════════════════════════════════════════════════════════════════════

Render tiene una política en el FREE TIER:
   • Si la app NO recibe tráfico en 15 minutos
   • Render la PAUSA automáticamente
   • Cuando recibe una solicitud, la DESPIERTA (tarda 30 seg)

PROBLEMA PARA BOTS:
   • Los bots ESPERAN mensajes (no generan tráfico)
   • Si nadie escribe en 15 minutos → app se pausa
   • Cuando escribes, tarda 30 segundos en responder
   • ¡Mala experiencia!


═══════════════════════════════════════════════════════════════════════════
💡 SOLUCIÓN: KEEP-ALIVE (Ping automático)
═══════════════════════════════════════════════════════════════════════════

¿Cómo funciona?

   1. Usamos un servicio externo (UptimeRobot) que es GRATUITO
   2. Este servicio hace "ping" a tu app cada cierto tiempo (ej: 5-10 min)
   3. El ping simula tráfico → Render ve actividad
   4. Render NO pausa porque detecta "uso"
   5. ¡Tu app siempre está despierta!

DIAGRAMA:
   ┌─────────────────┐
   │  UptimeRobot    │  (Servicio gratis)
   │  (Vigía)        │
   └────────┬────────┘
            │
            │ Ping cada 5 minutos
            │ GET https://tu-app.onrender.com
            ▼
   ┌─────────────────┐
   │    RENDER       │
   │   Tu App        │  ← "Hay tráfico" → No pausa
   └─────────────────┘


═══════════════════════════════════════════════════════════════════════════
🚀 PASO 1: CONFIGURAR UPTIMEROBOT (3 minutos)
═══════════════════════════════════════════════════════════════════════════

PASO 1.1: Crear cuenta
─────────────────────────────────────────────────────────────────────────
   1. ve a: https://uptimerobot.com
   2. Click "Sign Up" (arriba a la derecha)
   3. Usa email + contraseña (o conecta con Google)
   4. Verifica email
   5. ¡Listo! Estás adentro


PASO 1.2: Crear Monitor HTTP
─────────────────────────────────────────────────────────────────────────
   1. En el Dashboard, click "+ Add Monitor"
   
   2. Llena el formulario:

      TYPE:              HTTP(s)
      
      FRIENDLY NAME:     Mi Bot Telegram
                        (o cualquier nombre que quieras)
      
      URL:               https://tu-app-en-render.onrender.com
                        (Aquí necesitas tu URL de Render)
      
      MONITOR INTERVAL:  5 minutes
                        (Cada 5 minutos hace ping)
      
      ALERT CONTACTS:    Usa el email default (o agrega uno)
   
   3. Deja TODO LO DEMÁS como está (default)
   
   4. Click "CREATE MONITOR"


⚠️ IMPORTANTE: ¿DÓNDE CONSIGO LA URL DE RENDER?
─────────────────────────────────────────────────────────────────────────
   1. Ve a tu Dashboard de Render: https://dashboard.render.com
   2. Click en tu proyecto/servicio
   3. Arriba verás: "https://nombre-de-tu-app.onrender.com"
   4. ESA es la URL que necesitas en UptimeRobot

   Ejemplo:
   Si tu app se llama "bot-gastos", la URL será:
   https://bot-gastos.onrender.com


═══════════════════════════════════════════════════════════════════════════
✅ PASO 2: VERIFICAR QUE FUNCIONA (1 minuto)
═══════════════════════════════════════════════════════════════════════════

Una vez creado el monitor:

   1. En UptimeRobot Dashboard, verás tu monitor
   2. Debería mostrar: "Up" (verde)
   3. Si dice "Down" (rojo), revisa:
      • ¿La URL es correcta?
      • ¿Tu app en Render está running (no crashed)?
      • ¿Hay espacios en blanco en la URL?

   4. Click en el monitor para ver detalles
   5. Debería mostrar: "Response time: 200 OK" o similar


═══════════════════════════════════════════════════════════════════════════
🔄 CÓMO FUNCIONA AHORA
═══════════════════════════════════════════════════════════════════════════

Cada 5 minutos:
   1. UptimeRobot envía un "ping" a tu app
   2. Tu app recibe la solicitud (aunque sea vacía)
   3. Render ve: "Hay tráfico" 
   4. Render: "No pauso"
   5. Tu app sigue activa 24/7

RESULTADO:
   ✅ Bot disponible siempre
   ✅ Responde al instante (no tardanza)
   ✅ Recibe mensajes de Telegram sin demora
   ✅ GRATIS


═══════════════════════════════════════════════════════════════════════════
⚙️ CONFIGURACIÓN AVANZADA (Opcional pero útil)
═══════════════════════════════════════════════════════════════════════════

Si quieres optimizar el keep-alive:

OPCIÓN A: Ping más frecuente
   • Interval: 3 minutos (más seguro)
   • Ventaja: app nunca tendrá riesgo de pausarse
   • Desventaja: más pings innecesarios
   • ✅ RECOMENDADO

OPCIÓN B: Ping menos frecuente
   • Interval: 10 minutos (ahorra recursos)
   • Ventaja: menos solicitudes
   • Desventaja: riesgo teórico de pausa
   • ⚠️ No recomendado

OPCIÓN C: Scheduled Downtime (Para ahorrar batería)
   • UptimeRobot → Monitor → Customize
   • "Main Maintenance Windows"
   • Ej: No enviar pings de 00:00 a 06:00
   • Ventaja: app se pausa mientras no la usas
   • ✅ BUENA IDEA para ahorrar


═══════════════════════════════════════════════════════════════════════════
🎯 VERIFICACIÓN: ¿ESTÁ FUNCIONANDO?
═══════════════════════════════════════════════════════════════════════════

Para confirmar que el keep-alive funciona:

MÉTODO 1: Dejar pasar 16 minutos sin usar la app
───────────────────────────────────────────────────────────────────────────
   1. Sin keep-alive: app se hubiera pausado
   2. Con keep-alive: sigue respondiendo
   
   2. Abre Telegram
   3. Escribe /estado
   4. Debería responder en 1-2 segundos ✅


MÉTODO 2: Ver logs en Render
───────────────────────────────────────────────────────────────────────────
   1. Ve a tu proyecto en https://dashboard.render.com
   2. Click en "Logs" (lado izquierdo)
   3. Verás requests de UptimeRobot cada 5 minutos
   4. Esto confirma que funciona

   Verás algo como:
   [INFO] GET request from 192.168.x.x (UptimeRobot)
   [INFO] Ping received at 14:30:00
   [INFO] Keep-alive active


═══════════════════════════════════════════════════════════════════════════
⚠️ NOTAS Y LIMITACIONES
═══════════════════════════════════════════════════════════════════════════

✅ LO QUE FUNCIONA:
   • Mantiene la app siempre activa
   • Bot recibe mensajes sin demora
   • Completamente gratuito
   • Funciona en cualquier Render (free tier)
   • Escalable a otras apps

❌ LO QUE NO FUNCIONA:
   • UptimeRobot hace "GET" a tu app
   • Tu bot puede recibir esos GETs como "eventos"
   • Solución: Ignorar GETs de UptimeRobot en tu código

⚠️ IMPORTANTE: 
   El ping de UptimeRobot puede causar "ruido" en tus logs
   No es problema, pero puedes filtrar en tu código (te lo muestro)


═══════════════════════════════════════════════════════════════════════════
🛠️ CÓDIGO: IGNORAR PINGS DE UPTIMEROBOT (Por si acaso)
═══════════════════════════════════════════════════════════════════════════

Si notas que los pings de UptimeRobot causan errores, añade esto 
al inicio de main.py:

---CÓDIGO PYTHON---
import os
import logging
from flask import Flask, request

app = Flask(__name__)

# Endpoint básico para UptimeRobot (evita errores)
@app.route('/', methods=['GET'])
def health_check():
    user_agent = request.headers.get('User-Agent', '')
    
    # Si es de UptimeRobot, responde simple
    if 'UptimeRobot' in user_agent:
        return {'status': 'ok'}, 200
    
    # Si es otra cosa, puede procesarse
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

---FIN CÓDIGO---

NOTA: Tu bot actual (python-telegram-bot) NO necesita esto
      porque usa polling, no webhooks. Pero es bueno saberlo.


═══════════════════════════════════════════════════════════════════════════
📋 CHECKLIST DE CONFIGURACIÓN
═══════════════════════════════════════════════════════════════════════════

Antes de considerar terminado:

□ Crear cuenta en UptimeRobot
□ Crear monitor HTTP
□ Nombre: "Mi Bot Telegram" (o similar)
□ URL: https://tu-app-en-render.onrender.com
□ Interval: 5 minutes
□ Status en UptimeRobot: "Up" (verde)
□ Dejar pasar 15 minutos sin usar app
□ Escribir /estado en Telegram
□ Verifica que responde en 1-2 segundos
□ Ver logs en Render (debería haber pings cada 5 min)
□ ¡LISTO!


═══════════════════════════════════════════════════════════════════════════
🔄 PARA OTRAS APPS (Cómo reciclar esto)
═══════════════════════════════════════════════════════════════════════════

Este sistema funciona para CUALQUIER app en Render:

Pasos para otra app:
   1. Ve a UptimeRobot
   2. "+ Add Monitor"
   3. URL de la nueva app: https://nueva-app.onrender.com
   4. Interval: 5 minutes
   5. ¡Listo!

Puedes tener ILIMITADOS monitores en UptimeRobot free tier.
Cada uno con su URL.


═══════════════════════════════════════════════════════════════════════════
💰 COSTO TOTAL
═══════════════════════════════════════════════════════════════════════════

Render Free Tier:       $0/mes
UptimeRobot Free:       $0/mes
─────────────────────────────
TOTAL:                  $0/mes ✅

Con keep-alive, tu bot funciona 24/7 sin costar nada.


═══════════════════════════════════════════════════════════════════════════
🆘 TROUBLESHOOTING: Si algo no funciona
═══════════════════════════════════════════════════════════════════════════

PROBLEMA 1: UptimeRobot muestra "Down"
─────────────────────────────────────────────────────────────────────────
Soluciones:
   1. Verifica URL en UptimeRobot vs URL real en Render
   2. En Render, ¿está RUNNING la app? Verifica estado
   3. ¿Hay errores en logs de Render? 
   4. Prueba acceder a la URL en navegador (debe responder)
   5. Espera 5 minutos y refresca


PROBLEMA 2: Bot sigue pausándose
─────────────────────────────────────────────────────────────────────────
Soluciones:
   1. Verifica que Monitor esté "Up" (verde)
   2. Reduce Interval a 3 minutos (más agresivo)
   3. Revisa logs de Render (debería haber pings)
   4. Si no hay pings: UptimeRobot no conecta
      → Verifica URL nuevamente


PROBLEMA 3: Bot recibe muchos errores de UptimeRobot
─────────────────────────────────────────────────────────────────────────
Soluciones:
   1. Ignora User-Agent de UptimeRobot en tu código (vea arriba)
   2. O filtra en logs: solo muestra errores reales
   3. No es crítico (bot sigue funcionando)


PROBLEMA 4: No sé mi URL de Render
─────────────────────────────────────────────────────────────────────────
   1. Ve a https://dashboard.render.com
   2. Click en tu servicio/app
   3. Arriba a la derecha verás: nombre-de-app.onrender.com
   4. Cópialo completamente con https://


═══════════════════════════════════════════════════════════════════════════
✨ RESUMEN FINAL
═══════════════════════════════════════════════════════════════════════════

PROBLEMA ORIGINAL:
   ❌ Render pausa apps después de 15 minutos sin uso

SOLUCIÓN:
   ✅ UptimeRobot hace "ping" cada 5 minutos
   ✅ Render ve actividad
   ✅ App nunca se pausa

BENEFICIOS:
   ✅ Bot disponible 24/7
   ✅ Responde al instante
   ✅ GRATIS
   ✅ Funciona en cualquier Render

TIEMPO DE SETUP:
   ⏱️  5 minutos total

MANTENIMIENTO:
   🔧 Ninguno (automático)


═══════════════════════════════════════════════════════════════════════════

¡Listo! Ahora tu bot en Render estará siempre despierto. 🚀

Puedo ayudarte a configurarlo si necesitas. ¿También quieres que revise
tu código de Render para asegurar que está optimizado?

═══════════════════════════════════════════════════════════════════════════
"""
)

input("\nPresiona ENTER para cerrar...")
