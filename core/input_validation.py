"""Script de validación de inputs mejorado con ejemplos y sugerencias"""

import re
from config.settings import GENRES, LENGTH_OPTIONS, TONES


def validar_entrada(entrada: dict) -> tuple[bool, str]:
    """
    Verifica que todos los campos requeridos estén presentes, no vacíos y sean válidos.
    Devuelve (estado, mensaje de validación).
    """

    campos_requeridos = [
        "personajes",
        "escenario",
        "género",
        "elementos_trama",
        "tono",
        "longitud",
    ]

    for campo in campos_requeridos:
        if campo not in entrada or not entrada[campo]:
            return False, f"❌ Falta el campo requerido: '{campo}'."

    # Validar 'personajes'
    personajes = entrada["personajes"].strip()
    if len(personajes) < 5:
        return (
            False,
            "❌ El campo 'personajes' debe tener al menos 5 caracteres. Ej: 'Lina, una científica curiosa y valiente.'",
        )
    if re.match(r"^[0-9\s,]+$", personajes):
        return (
            False,
            "❌ El campo 'personajes' no puede ser solo números o signos. Ej: 'Pedro, un ladrón astuto y reservado.'",
        )

    # Validar 'escenario'
    escenario = entrada["escenario"].strip()
    if len(escenario) < 5:
        return (
            False,
            "❌ El campo 'escenario' debe describir una época o lugar. Ej: 'Un futuro post-apocalíptico en Marte.'",
        )

    # Validar listas cerradas
    if entrada["género"] not in GENRES:
        return (
            False,
            f"❌ El género '{entrada['género']}' no es válido. Opciones: {', '.join(GENRES)}",
        )
    if entrada["tono"] not in TONES:
        return (
            False,
            f"❌ El tono '{entrada['tono']}' no es válido. Opciones: {', '.join(TONES)}",
        )
    if entrada["longitud"] not in LENGTH_OPTIONS:
        return (
            False,
            f"❌ La longitud '{entrada['longitud']}' no es válida. Opciones: {', '.join(LENGTH_OPTIONS)}",
        )

    # Validar elementos de trama
    trama = entrada["elementos_trama"]
    for clave in ["conflicto", "obstaculos", "resolucion"]:
        valor = trama.get(clave, "").strip()
        if len(valor) < 5:
            ejemplos = {
                "conflicto": "Ej: El protagonista descubre una conspiración intergaláctica.",
                "obstaculos": "Ej: Debe cruzar un desierto vigilado por robots asesinos.",
                "resolucion": "Ej: La verdad se revela y los aliados restauran la paz.",
            }
            return (
                False,
                f"❌ El elemento de trama '{clave}' debe tener al menos 5 caracteres. {ejemplos[clave]}",
            )

    return True, "✅ Entrada válida."


def limpiar_texto(texto: str) -> str:
    """Preprocesa texto libre (ej. quitar caracteres innecesarios, espacios, etc.)"""
    return texto.strip()
