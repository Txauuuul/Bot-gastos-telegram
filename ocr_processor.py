"""
Módulo para OCR de tickets.
Soporta Google Cloud Vision (recomendado) y Tesseract como fallback.
"""

import logging
import os
from typing import Optional, Dict, List
from pathlib import Path

logger = logging.getLogger(__name__)

# Por defecto, intentamos usar Google Cloud Vision
USE_GOOGLE_VISION = True


def extraer_texto_vision(imagen_path: str) -> Optional[str]:
    """
    Extrae texto de una imagen usando Google Cloud Vision API.

    Args:
        imagen_path: Ruta a la imagen

    Returns:
        Texto extraído o None si falla

    Requisitos:
    - pip install google-cloud-vision
    - archivo de credenciales: credentials.json
    """
    try:
        from google.cloud import vision

        client = vision.ImageAnnotatorClient()

        with open(imagen_path, "rb") as f:
            content = f.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            return texts[0].description
        return None

    except ImportError:
        logger.warning("❌ google-cloud-vision no instalado")
        return None
    except Exception as e:
        logger.error(f"❌ Error en Google Cloud Vision: {e}")
        return None


def extraer_texto_tesseract(imagen_path: str) -> Optional[str]:
    """
    Extrae texto de una imagen usando Tesseract (OCR local).

    Args:
        imagen_path: Ruta a la imagen

    Returns:
        Texto extraído o None si falla

    Requisitos:
    - pip install pytesseract pillow
    - Descargar Tesseract desde: https://github.com/UB-Mannheim/tesseract/wiki
    """
    try:
        import pytesseract
        from PIL import Image

        # En Windows, configurar ruta a Tesseract si es necesario
        # pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        imagen = Image.open(imagen_path)
        texto = pytesseract.image_to_string(imagen, lang="spa")  # Español
        return texto if texto.strip() else None

    except ImportError:
        logger.warning("❌ pytesseract o Pillow no instalados")
        return None
    except Exception as e:
        logger.error(f"❌ Error en Tesseract: {e}")
        return None


async def procesar_ticket(
    imagen_path: str, metodo: str = "auto"
) -> Optional[Dict[str, str]]:
    """
    Procesa un ticket usando OCR.

    Args:
        imagen_path: Ruta a la imagen del ticket
        metodo: 'vision' (Google Cloud), 'tesseract' (local), 'auto' (intenta ambos)

    Returns:
        Dict con 'texto' extraído o None si falla
    """
    if not os.path.exists(imagen_path):
        logger.error(f"❌ Imagen no encontrada: {imagen_path}")
        return None

    texto = None

    if metodo in ["auto", "vision"]:
        logger.info("🔍 Intentando OCR con Google Cloud Vision...")
        texto = extraer_texto_vision(imagen_path)
        if texto:
            logger.info("✅ Texto extraído con Google Cloud Vision")
            return {"texto": texto, "metodo": "vision"}

    if metodo in ["auto", "tesseract"] and not texto:
        logger.info("🔍 Intentando OCR con Tesseract (local)...")
        texto = extraer_texto_tesseract(imagen_path)
        if texto:
            logger.info("✅ Texto extraído con Tesseract")
            return {"texto": texto, "metodo": "tesseract"}

    if not texto:
        logger.warning("❌ No se pudo extraer texto del ticket con ningún método")
        return None

    return {"texto": texto, "metodo": "fallback"}


def parseador_ticket(texto_extraido: str) -> List[Dict[str, str]]:
    """
    Parsea el texto extraído de un ticket para obtener líneas de compra.

    Args:
        texto_extraido: Texto del OCR

    Returns:
        Lista de líneas de compra con formato {"concepto": "", "precio": ""}
    """
    lineas = []

    import re

    for linea in texto_extraido.split("\n"):
        linea = linea.strip()
        if not linea:
            continue

        # Buscar patrón: "Descripción 5.50€" o "Descripción 5.50 EUR"
        match = re.search(
            r"^(.+?)\s+(\d+[.,]\d{1,2})\s*(?:€|EUR)?$", linea
        )

        if match:
            concepto = match.group(1).strip()
            precio = match.group(2).replace(",", ".")

            lineas.append({"concepto": concepto, "precio": precio})

    return lineas


# Ejemplo de uso
if __name__ == "__main__":
    import asyncio

    logging.basicConfig(level=logging.INFO)

    # Probar con una imagen (reemplazar con una real)
    imagen_test = "ticket.jpg"

    if os.path.exists(imagen_test):
        resultado = asyncio.run(procesar_ticket(imagen_test))
        if resultado:
            print(f"Texto extraído:\n{resultado['texto']}\n")
            lineas = parseador_ticket(resultado["texto"])
            print(f"Líneas de compra: {lineas}")
    else:
        print(f"Imagen de prueba no encontrada: {imagen_test}")
