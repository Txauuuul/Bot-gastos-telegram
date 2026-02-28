"""
Script para obtener las credenciales OAuth de Google Drive.
Ejecuta este script UNA SOLA VEZ en tu PC para obtener el refresh token.
Luego añade los valores a las variables de entorno de Render.

PASOS PREVIOS:
1. Ve a https://console.cloud.google.com/
2. Selecciona tu proyecto
3. APIs y servicios → Credenciales → + CREAR CREDENCIAL → ID de cliente OAuth 2.0
4. Tipo de aplicación: "Aplicación de escritorio"
5. Descarga el JSON y renómbralo a "oauth_credentials.json" en esta carpeta

EXECUTE:
    python obtener_token_drive.py
"""

import json
import os
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Instalando dependencias...")
    os.system("pip install google-auth-oauthlib")
    from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
BASE_DIR = Path(__file__).parent
OAUTH_FILE = BASE_DIR / "oauth_credentials.json"

if not OAUTH_FILE.exists():
    print("❌ No se encontró 'oauth_credentials.json'.")
    print()
    print("Pasos:")
    print("1. Ve a https://console.cloud.google.com/")
    print("2. APIs y servicios → Credenciales")
    print("3. + CREAR CREDENCIAL → ID de cliente OAuth 2.0")
    print("4. Tipo: 'Aplicación de escritorio', ponle nombre 'Bot Gastos'")
    print("5. Descarga el JSON → renómbralo 'oauth_credentials.json'")
    print("6. Ponlo en la misma carpeta que este script")
    print("7. Vuelve a ejecutar: python obtener_token_drive.py")
    exit(1)

# Verificar que no sea Service Account
with open(OAUTH_FILE) as f:
    data = json.load(f)

if data.get("type") == "service_account":
    print("❌ El archivo es un Service Account, no sirve para este proceso.")
    print("   Necesitas crear un 'ID de cliente OAuth 2.0' (tipo Aplicación de escritorio).")
    exit(1)

print("🔐 Abriendo navegador para autenticar con Google...")
print("   (Si no se abre, copia el enlace que aparece en pantalla)")
print()

flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_FILE), SCOPES)
creds = flow.run_local_server(port=0)

print()
print("=" * 60)
print("✅ ¡Autenticación completada! Copia estos valores en Render:")
print("=" * 60)
print()

client_info = data.get("installed") or data.get("web", {})
print(f"GOOGLE_CLIENT_ID     = {client_info.get('client_id', '')}")
print(f"GOOGLE_CLIENT_SECRET = {client_info.get('client_secret', '')}")
print(f"GOOGLE_REFRESH_TOKEN = {creds.refresh_token}")
print()
print("=" * 60)
print("En Render → Environment → añade esas 3 variables")
print("=" * 60)
