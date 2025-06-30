"""Script de validación de inputs"""

import re

from config.settings import GENRES, LENGTH_OPTIONS, TONES


def validar_entrada(entrada: dict) -> tuple[bool, str]:
    """
    Verifica que todos los campos requeridos están presentes, no vacíos y son válidos.
    """

    campos_requeridos = [
        "personajes",
        "escenario",
        "género",
        "elementos_trama",
        "tono",
        "longitud",
    ]

    # 1. Presencia y no vacío
    for campo in campos_requeridos:
        if campo not in entrada or not entrada[campo]:
            return False, f"❌ Falta el campo: {campo}"

    # 2. Tipo y contenido básico
    if (
        not isinstance(entrada["personajes"], str)
        or len(entrada["personajes"].strip()) < 5
    ):
        return (
            False,
            "❌ El campo 'personajes' debe ser una descripción de al menos 5 caracteres.",
        )

    if re.match(r"^[0-9\s,]+$", entrada["personajes"]):
        return (
            False,
            "❌ 'personajes' no puede ser solo números o caracteres sin significado.",
        )

    if (
        not isinstance(entrada["escenario"], str)
        or len(entrada["escenario"].strip()) < 5
    ):
        return False, "❌ El 'escenario' debe describir una época, lugar o atmósfera."

    # 3. Validación de listas cerradas (género, tono, longitud)
    if entrada["género"] not in GENRES:
        return False, f"❌ El género '{entrada['género']}' no es válido."

    if entrada["tono"] not in TONES:
        return False, f"❌ El tono '{entrada['tono']}' no es válido."

    if entrada["longitud"] not in LENGTH_OPTIONS:
        return False, f"❌ La longitud '{entrada['longitud']}' no es válida."

    # 4. Validar estructura de elementos_trama
    trama = entrada["elementos_trama"]
    for clave in ["conflicto", "obstaculos", "resolucion"]:
        if clave not in trama or not trama[clave].strip():
            return False, f"❌ Falta el elemento de trama: {clave}"
        if len(trama[clave].strip()) < 5:
            return False, f"❌ El {clave} debe tener al menos 5 caracteres."

    return True, "✅ Entrada válida"


def limpiar_texto(texto: str) -> str:
    """
    Preprocesa texto libre (ej. quitar caracteres innecesarios, espacios, etc.)
    """
    return texto.strip()
