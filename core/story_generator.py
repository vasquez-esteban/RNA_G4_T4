"""Script de generación de historia"""

# import openai
from config.settings import DEFAULT_MODEL, OPENAI_API_KEY

# openai.api_key = OPENAI_API_KEY


def generar_historia(prompt: str) -> str:
    """
    Llama al modelo LLM con el prompt y devuelve la historia generada.
    Descomenta esta función cuando estés listo para usar la API real.
    """
    # response = openai.ChatCompletion.create(
    #     model=DEFAULT_MODEL,
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.8,
    #     max_tokens=1500,
    # )
    # return response["choices"][0]["message"]["content"]
    raise NotImplementedError(
        "Función real desactivada. Usa generar_historia_mock() para pruebas."
    )


def generar_historia_mock(prompt: str) -> str:
    """
    Devuelve una historia simulada para pruebas sin conexión a la API.
    """
    print("📤 Prompt recibido por la función mock:")
    print(prompt)  # Esto se verá en la terminal
    print("Llave recibida por la función mock:")
    print(OPENAI_API_KEY)

    return (
        "Había una vez en un lejano reino de fantasía, una joven valiente llamada Liria que "
        "soñaba con cambiar el destino de su aldea. ..."
    )
