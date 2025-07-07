from openai import OpenAI
from config.settings import OPENROUTER_API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def generar_historia(prompt: str) -> str:
    """
    Llama al modelo LLM con el prompt y devuelve la historia generada.
    """
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        extra_headers={
            "HTTP-Referer": "http://https://rna-g4-generador-historias.streamlit.app/",
            "X-Title": "AgenteHistorias",
        },
    )
    return response.choices[0].message.content
