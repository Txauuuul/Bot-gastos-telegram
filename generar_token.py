"""
Script para generar token.json de Google Drive.
Ejecuta este script UNA VEZ localmente para autenticarte.
"""
import os
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

if not os.path.exists("credentials.json"):
    print("❌ No se encontró credentials.json en esta carpeta.")
    print("   Descárgalo desde Google Cloud Console y ponlo aquí.")
    exit(1)

print("🔐 Iniciando autenticación con Google Drive...")
print("   Se abrirá el navegador. Si no se abre, copia la URL que aparece abajo.\n")

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

# open_browser=True fuerza el intento, si falla imprime la URL
creds = flow.run_local_server(port=8080, open_browser=True)

with open("token.json", "w") as token:
    token.write(creds.to_json())

print("\n✅ token.json generado correctamente.")
print("   Ya puedes usar Google Drive con el bot.")
print("   Sube el token.json a Render como Secret File.")
