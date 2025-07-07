"""Script de configuración"""

import streamlit as st

# Clave API
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Parámetros de generación
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"
TEMPERATURE = 0.8
MAX_TOKENS = 1500

# Opciones válidas para entrada de usuario
GENRES = [
    "Fantasía",
    "Misterio",
    "Romance",
    "Terror",
    "Ciencia Ficción",
    "Comedia",
    "Aventura",
]

TONES = ["Humorístico", "Oscuro", "Caprichoso", "Dramático", "Satírico"]

LENGTH_OPTIONS = {"Corta": (300, 400), "Mediana": (400, 600), "Larga": (600, 800)}
