"""Script de construcción de Prompt"""

INSTRUCCIONES_POR_GENERO = {
    "Fantasía": "Incluye elementos de magia, criaturas míticas y un mundo imaginario.",
    "Misterio": "Plantea un enigma o crimen. Deja pistas y resuelve el misterio al final.",
    "Romance": "Desarrolla una historia centrada en una relación emocional y sus conflictos.",
    "Terror": "Crea tensión y miedo. Usa atmósferas oscuras, suspenso y sorpresas.",
    "Ciencia ficción": "Incluye tecnología avanzada o viajes en el tiempo en un futuro posible.",
    "Comedia": "Usa situaciones graciosas y lenguaje humorístico para entretener.",
    "Aventura": "Desarrolla una misión o viaje con riesgos, exploración y acción.",
}

INSTRUCCIONES_LONGITUD = {
    "Corta": "Tu historia debe tener entre 300 y 400 palabras exactamente. Sé preciso. No superes ese rango.",
    "Mediana": "Tu historia debe tener entre 400 y 600 palabras exactamente. Sé preciso. Mantén un desarrollo intermedio.",
    "Larga": "Tu historia debe tener entre 600 y 800 palabras. Sé preciso. Expándete con más detalle y profundidad narrativa, pero no superes el rango de palabras",
}


def construir_prompt(entrada_usuario: dict) -> str:
    genero = entrada_usuario.get("género", "Fantasía")
    tono = entrada_usuario.get("tono", "Dramático")
    longitud = entrada_usuario.get("longitud", "Mediana")
    personajes = entrada_usuario.get("personajes", "")
    escenario = entrada_usuario.get("escenario", "")
    elementos = entrada_usuario.get("elementos_trama", {})
    conflicto = elementos.get("conflicto", "")
    obstaculos = elementos.get("obstaculos", "")
    resolucion = elementos.get("resolucion", "")
    tiene_dialogo = entrada_usuario.get("incluir_dialogo")

    instrucciones_genero = INSTRUCCIONES_POR_GENERO.get(genero, "")
    instrucciones_longitud = INSTRUCCIONES_LONGITUD.get(longitud, "")

    prompt_final = f"""
Eres un escritor profesional especializado en cuentos del género **{genero}**, con un tono **{tono}**.

Tu objetivo es escribir una historia original y atractiva. {instrucciones_longitud}

🎯 Consideraciones específicas para este género:
{instrucciones_genero}

🧭 Estructura sugerida:
1. **Introducción:** Presenta el escenario y a los personajes.
2. **Desarrollo:** Introduce el conflicto y los obstáculos.
3. **Resolución:** Cierra la historia con una conclusión satisfactoria.

🧍 **Personajes:** {personajes}
🌍 **Escenario:** {escenario}
⚔️ **Conflicto:** {conflicto}
🧱 **Obstáculos:** {obstaculos}
🔓 **Resolución esperada:** {resolucion}

📚 Comienza la historia a continuación:

⚠️ Importante: La historia debe ser apropiada para todos los públicos. No incluyas lenguaje sexual, escenas violentas, contenido explícito, discriminación ni situaciones perturbadoras. Mantén un tono respetuoso y seguro.
"""
    if tiene_dialogo:
        prompt_final += "\n\n🗣️ Instrucción adicional: Asegúrate de incluir diálogos realistas entre los personajes, usando comillas o guiones. El diálogo debe aportar al desarrollo del conflicto y a la caracterización."

    return prompt_final.strip()


def construir_prompt_continuacion(historia_previa: str, entrada_usuario: dict) -> str:
    genero = entrada_usuario.get("género", "Fantasía")
    tono = entrada_usuario.get("tono", "Dramático")
    instrucciones_genero = INSTRUCCIONES_POR_GENERO.get(genero, "")

    prompt = f"""
Eres un escritor del género **{genero}** con un tono **{tono}**.

Tu tarea es continuar una historia existente manteniendo coherencia con los personajes, el conflicto y el estilo narrativo ya usado.

{instrucciones_genero}

Historia anterior:
\"\"\"
{historia_previa}
\"\"\"

Continúa la historia justo donde terminó, agregando nuevos eventos, complicaciones o resolución alternativa si aplica:
"""
    return prompt.strip()
