"""Script de construcción de Prompt"""


def construir_prompt(entrada_usuario: dict) -> str:
    """
    Construye un prompt detallado para el LLM en función de los elementos narrativos.
    """

    genero = entrada_usuario.get("género", "Fantasía")
    tono = entrada_usuario.get("tono", "Dramático")
    longitud = entrada_usuario.get("longitud", "Mediana")
    personajes = entrada_usuario.get("personajes", "")
    escenario = entrada_usuario.get("escenario", "")
    elementos = entrada_usuario.get("elementos_trama", {})

    conflicto = elementos.get("conflicto", "")
    obstaculos = elementos.get("obstaculos", "")
    resolucion = elementos.get("resolucion", "")

    prompt_final = f"""
Eres un escritor profesional de cuentos del género **{genero}** con un tono **{tono}**.
Tu tarea es escribir una historia original de longitud **{longitud}** (entre 300 y 800 palabras).

Sigue esta estructura narrativa:
1. Introducción: Presenta el escenario y a los personajes.
2. Desarrollo: Introduce el conflicto y los obstáculos que enfrentan.
3. Resolución: Cierra la historia de forma coherente con una resolución clara.

🧍 Personajes:
{personajes}

🌍 Escenario:
{escenario}

⚔️ Conflicto:
{conflicto}

🧱 Obstáculos:
{obstaculos}

🔓 Resolución esperada:
{resolucion}

Comienza la historia ahora:
"""
    return prompt_final.strip()
