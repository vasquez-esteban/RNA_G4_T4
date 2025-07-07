"""Módulo principal de la web"""

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st

from config.settings import GENRES, LENGTH_OPTIONS, TONES
from core.input_validation import validar_entrada
from core.prompt_engineering import construir_prompt
from core.story_generator import generar_historia

st.set_page_config(page_title="Agente de Historias", layout="centered")
st.title("📖 Agente Creativo de Historias")


# Inicializar session_state
if "historia" not in st.session_state:
    st.session_state.historia = ""
if "entrada" not in st.session_state:
    st.session_state.entrada = {}

# Formulario de entrada
with st.form("story_form"):
    personajes = st.text_area(
        "👥 Personajes (nombre, rol, rasgos)",
        value=st.session_state.entrada.get("personajes", ""),
        height=100,
    )
    escenario = st.text_area(
        "🌍 Escenario (época, lugar, atmósfera)",
        value=st.session_state.entrada.get("escenario", ""),
        height=100,
    )
    genero = st.selectbox(
        "🎭 Género",
        GENRES,
        index=GENRES.index(st.session_state.entrada.get("género", GENRES[0])),
    )
    tono = st.selectbox(
        "🎨 Tono",
        TONES,
        index=TONES.index(st.session_state.entrada.get("tono", TONES[0])),
    )
    conflicto = st.text_input(
        "⚔️ Conflicto central", value=st.session_state.entrada.get("conflicto", "")
    )
    obstaculos = st.text_input(
        "🧱 Obstáculos principales",
        value=st.session_state.entrada.get("obstaculos", ""),
    )
    resolucion = st.text_input(
        "🔓 Resolución esperada", value=st.session_state.entrada.get("resolucion", "")
    )
    longitud = st.radio(
        "📏 Longitud deseada",
        list(LENGTH_OPTIONS.keys()),
        index=list(LENGTH_OPTIONS.keys()).index(
            st.session_state.entrada.get("longitud", "Mediana")
        ),
    )

    submitted = st.form_submit_button("Generar Historia")

if submitted:
    entrada = {
        "personajes": personajes,
        "escenario": escenario,
        "género": genero,
        "tono": tono,
        "elementos_trama": {
            "conflicto": conflicto,
            "obstaculos": obstaculos,
            "resolucion": resolucion,
        },
        "longitud": longitud,
    }
    st.session_state.entrada = {
        "personajes": personajes,
        "escenario": escenario,
        "género": genero,
        "tono": tono,
        "conflicto": conflicto,
        "obstaculos": obstaculos,
        "resolucion": resolucion,
        "longitud": longitud,
    }

    es_valida, mensaje = validar_entrada(entrada)

    if not es_valida:
        st.error(mensaje)
    else:
        with st.spinner("Generando historia..."):
            prompt = construir_prompt(entrada)
            historia = generar_historia(prompt)
            st.success("¡Historia generada!")
            st.session_state.historia = historia

# Mostrar historia y botón de descarga
if st.session_state.historia:
    st.text_area("📚 Historia completa", st.session_state.historia, height=400)
    st.download_button(
        label="📥 Descargar Historia",
        data=st.session_state.historia,
        file_name="historia_generada.txt",
        mime="text/plain",
    )
