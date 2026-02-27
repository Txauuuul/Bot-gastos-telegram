"""
Módulo para parsear gastos en texto.
Interpreta líneas como "Patatas 2.50€" y extrae concepto, precio y fecha.
"""

import re
from datetime import datetime
from typing import Optional, Tuple, Dict


class ExpenseParser:
    """Clase para parsear strings de gastos con formato flexible."""

    # Patrones regex para diferentes formatos
    PATTERNS = [
        # "Patatas 2.50€" o "Patatas 2.50 €" o "Patatas 2€" o "Patatas 2"
        r"^([a-zA-Z\s]+?)\s+(\d+(?:[.,]\d{1,2})?)\s*€?$",
        # "Patatas: 2.50€" o "Patatas: 2€" o "Patatas: 2"
        r"^([a-zA-Z\s]+?):\s*(\d+(?:[.,]\d{1,2})?)\s*€?$",
        # "2.50€ Patatas" o "2€ Patatas" o "2 Patatas"
        r"^(\d+(?:[.,]\d{1,2})?)\s*€?\s+([a-zA-Z\s]+?)$",
        # "Patatas - 2.50 €" o "Patatas - 2€" o "Patatas - 2"
        r"^([a-zA-Z\s]+?)\s*-\s*(\d+(?:[.,]\d{1,2})?)\s*€?$",
    ]

    # Palabras clave para detectar ingresos
    INCOME_KEYWORDS = ["ingreso", "cobro", "ganancia", "entrada", "dinero", "sueldo", "paga", "bonus"]

    @staticmethod
    def _detectar_ingreso(texto: str) -> bool:
        """
        Detecta si el texto indica un ingreso.
        
        Args:
            texto: String a analizar
            
        Returns:
            True si es un ingreso, False si no
        """
        texto_lower = texto.lower()
        
        # Detectar símbolos: +50 o 50+
        if texto.startswith("+") or texto.endswith("+"):
            return True
        
        # Detectar palabras clave
        for keyword in ExpenseParser.INCOME_KEYWORDS:
            if keyword in texto_lower:
                return True
        
        return False

    @staticmethod
    def parse(texto: str, forzar_ingreso: bool = False) -> Optional[Dict[str, str | float]]:
        """
        Parsea un string de gasto o ingreso y extrae concepto, precio y fecha.

        Args:
            texto: String con formato como "Patatas 2.50€" o "+50 Ingreso"
            forzar_ingreso: Si True, trata el texto como ingreso

        Returns:
            Dict con claves: concepto, precio (float), fecha, hora, formato_original, es_ingreso
            o None si no coincide con ningún patrón
        """
        texto = texto.strip()
        es_ingreso = forzar_ingreso or ExpenseParser._detectar_ingreso(texto)
        
        # Limpiar símbolos de ingreso para parsear
        texto_limpio = texto.lstrip("+").rstrip("+").strip()

        for pattern in ExpenseParser.PATTERNS:
            match = re.match(pattern, texto_limpio)
            if match:
                grupos = match.groups()

                # Determinar cuál es concepto y cuál es precio
                if grupos[0].isdigit() or "." in grupos[0] or "," in grupos[0]:
                    precio_str = grupos[0]
                    concepto = grupos[1].strip().title()
                else:
                    concepto = grupos[0].strip().title()
                    precio_str = grupos[1]

                try:
                    # Normalizar precio: cambiar coma por punto
                    precio_normalizado = precio_str.replace(",", ".")
                    precio = float(precio_normalizado)
                    
                    # Si es ingreso, hacer el precio negativo para que reste del total
                    if es_ingreso:
                        precio = -abs(precio)
                        concepto = f"🟢 INGRESO: {concepto}"

                    fecha_hoy = datetime.now()

                    return {
                        "concepto": concepto,
                        "precio": precio,
                        "fecha": fecha_hoy.strftime("%d/%m/%Y"),
                        "hora": fecha_hoy.strftime("%H:%M:%S"),
                        "formato_original": texto,
                        "es_ingreso": es_ingreso,
                    }
                except ValueError:
                    return None

        return None

    @staticmethod
    def validar_gasto(gasto: Dict) -> Tuple[bool, str]:
        """
        Valida que un gasto o ingreso tenga los campos necesarios.

        Args:
            gasto: Diccionario con concepto, precio, fecha

        Returns:
            Tupla (es_válido: bool, mensaje: str)
        """
        if not gasto:
            return False, "❌ No se pudo procesar. Usa formato: 'Artículo 2' o '+50' para ingresos"

        if not gasto.get("concepto"):
            return False, "❌ Falta el concepto del gasto/ingreso (ej: 'Patatas')"

        precio = gasto.get("precio")
        if not precio or precio == 0:
            return False, "❌ Precio inválido. Debe ser diferente a 0€"

        return True, "✅ Gasto/Ingreso válido"


# Ejemplo de uso
if __name__ == "__main__":
    test_casos = [
        "Patatas 2.50€",
        "Leche 1.20 €",
        "Pan: 0.90€",
        "3.45€ Manzanas",
        "Agua - 2,30 €",
        "Patatas 1€",          # Precio redondo con €
        "Leche 1",             # Precio redondo sin €
        "Pan: 0.90",           # Sin €
        "2.50 Manzanas",       # Sin €
        "Agua - 2",            # Precio redondo sin €
    ]

    for caso in test_casos:
        resultado = ExpenseParser.parse(caso)
        print(f"\nInput: '{caso}'")
        print(f"Output: {resultado}")
        if resultado:
            es_válido, msg = ExpenseParser.validar_gasto(resultado)
            print(f"Validación: {msg}")
