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

    @staticmethod
    def parse(texto: str) -> Optional[Dict[str, str | float]]:
        """
        Parsea un string de gasto y extrae concepto, precio y fecha.

        Args:
            texto: String con formato como "Patatas 2.50€"

        Returns:
            Dict con claves: concepto, precio (float), fecha, formato_original
            o None si no coincide con ningún patrón
        """
        texto = texto.strip()

        for pattern in ExpenseParser.PATTERNS:
            match = re.match(pattern, texto)
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

                    fecha_hoy = datetime.now()

                    return {
                        "concepto": concepto,
                        "precio": precio,
                        "fecha": fecha_hoy.strftime("%d/%m/%Y"),
                        "hora": fecha_hoy.strftime("%H:%M:%S"),
                        "formato_original": texto,
                    }
                except ValueError:
                    return None

        return None

    @staticmethod
    def validar_gasto(gasto: Dict) -> Tuple[bool, str]:
        """
        Valida que un gasto tenga los campos necesarios.

        Args:
            gasto: Diccionario con concepto, precio, fecha

        Returns:
            Tupla (es_válido: bool, mensaje: str)
        """
        if not gasto:
            return False, "❌ No se pudo procesar el gasto. Usa formato: 'Artículo 2' o 'Artículo 2.50€'"

        if not gasto.get("concepto"):
            return False, "❌ Falta el concepto del gasto (ej: 'Patatas')"

        if not gasto.get("precio") or gasto["precio"] <= 0:
            return False, "❌ Precio inválido. Debe ser mayor a 0€"

        return True, "✅ Gasto válido"


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
