"""Módulo principal de la web con función de continuación de historias y control de botones"""

import sys
from pathlib import Path
import json

# Agregar la raíz del proyecto al path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st

from config.settings import GENRES, LENGTH_OPTIONS, TONES
from core.input_validation import validar_entrada
from core.prompt_engineering import construir_prompt, construir_prompt_continuacion
from core.story_generator import generar_historia
from core.filter_content import contiene_contenido_sensible


# Configuración de archivos
CONFIG_DIR = Path(__file__).resolve().parent / "user_configs"
CONFIG_FILE = CONFIG_DIR / "configuraciones_favoritas.json"


# Funciones de persistencia
def crear_directorio_config():
    """Crea el directorio de configuraciones si no existe"""
    CONFIG_DIR.mkdir(exist_ok=True)


def cargar_configuraciones_desde_archivo():
    """Carga las configuraciones desde el archivo JSON"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
        st.error(f"Error al cargar configuraciones: {e}")
        return {}


def guardar_configuraciones_en_archivo(configuraciones):
    """Guarda las configuraciones en el archivo JSON"""
    try:
        crear_directorio_config()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(configuraciones, f, indent=2, ensure_ascii=False)
        return True
    except (PermissionError, OSError) as e:
        st.error(f"Error al guardar configuraciones: {e}")
        return False


# Funciones de utilidad para configuraciones favoritas
def inicializar_session_state():
    """Inicializa todas las variables de session_state necesarias"""
    if "historia" not in st.session_state:
        st.session_state.historia = ""
    if "entrada" not in st.session_state:
        st.session_state.entrada = {}
    if "generando" not in st.session_state:
        st.session_state.generando = False
    if "configuraciones_favoritas" not in st.session_state:
        # Cargar configuraciones desde archivo al inicializar
        st.session_state.configuraciones_favoritas = (
            cargar_configuraciones_desde_archivo()
        )


def obtener_configuracion_actual():
    """Extrae la configuración actual del formulario"""
    return {
        "personajes": st.session_state.entrada.get("personajes", ""),
        "escenario": st.session_state.entrada.get("escenario", ""),
        "género": st.session_state.entrada.get("género", GENRES[0]),
        "tono": st.session_state.entrada.get("tono", TONES[0]),
        "conflicto": st.session_state.entrada.get("conflicto", ""),
        "obstaculos": st.session_state.entrada.get("obstaculos", ""),
        "resolucion": st.session_state.entrada.get("resolucion", ""),
        "longitud": st.session_state.entrada.get("longitud", "Mediana"),
        "incluir_dialogo": st.session_state.entrada.get("incluir_dialogo", False),
    }


def guardar_configuracion_favorita(nombre, config):
    """Guarda una configuración como favorita"""
    st.session_state.configuraciones_favoritas[nombre] = config.copy()
    # Guardar en archivo inmediatamente
    success = guardar_configuraciones_en_archivo(
        st.session_state.configuraciones_favoritas
    )
    return success


def cargar_configuracion_favorita(nombre):
    """Carga una configuración favorita"""
    if nombre in st.session_state.configuraciones_favoritas:
        config = st.session_state.configuraciones_favoritas[nombre]
        st.session_state.entrada = config.copy()
        return True
    return False


def eliminar_configuracion_favorita(nombre):
    """Elimina una configuración favorita"""
    if nombre in st.session_state.configuraciones_favoritas:
        del st.session_state.configuraciones_favoritas[nombre]
        # Guardar cambios en archivo
        success = guardar_configuraciones_en_archivo(
            st.session_state.configuraciones_favoritas
        )
        return success
    return False


def obtener_nombres_configuraciones():
    """Obtiene los nombres de todas las configuraciones favoritas"""
    return list(st.session_state.configuraciones_favoritas.keys())


def verificar_contenido_usuario(entrada):
    """Verifica solo el contenido proporcionado por el usuario"""
    textos_usuario = [
        entrada.get("personajes", ""),
        entrada.get("escenario", ""),
        entrada.get("elementos_trama", {}).get("conflicto", ""),
        entrada.get("elementos_trama", {}).get("obstaculos", ""),
        entrada.get("elementos_trama", {}).get("resolucion", ""),
    ]

    for texto in textos_usuario:
        if texto.strip() and contiene_contenido_sensible(texto):
            return True
    return False


def procesar_generacion_historia(entrada):
    """Procesa la generación de una nueva historia"""
    # Validar solo la entrada del usuario, no el prompt completo
    if verificar_contenido_usuario(entrada):
        st.error(
            "⚠️ Tu entrada contiene elementos sensibles o inapropiados. "
            "Por favor modifica la descripción y vuelve a intentarlo."
        )
        return False

    try:
        prompt = construir_prompt(entrada)
        historia = generar_historia(prompt)

        # Opcional: filtrar la historia generada también
        if contiene_contenido_sensible(historia):
            st.error(
                "⚠️ La historia generada contiene contenido sensible. Intenta con otros parámetros."
            )
            return False

        st.session_state.historia = historia
        st.success("¡Historia generada!")
        return True
    except RuntimeError as err:
        st.error(str(err))
        return False


def procesar_continuacion_historia():
    """Procesa la continuación de una historia existente"""
    # No filtrar el prompt de continuación, solo verificar la historia previa si es necesario
    try:
        prompt_cont = construir_prompt_continuacion(
            historia_previa=st.session_state.historia,
            entrada_usuario=st.session_state.entrada,
        )

        nueva_parte = generar_historia(prompt_cont)

        # Filtrar solo la nueva parte generada
        if contiene_contenido_sensible(nueva_parte):
            st.error(
                "⚠️ La continuación generada contiene contenido sensible. Intenta regenerar."
            )
            return False

        st.session_state.historia += "\n\n🧩 Continuación:\n" + nueva_parte
        st.success("¡Historia continuada!")
        return True
    except RuntimeError as err:
        st.error(str(err))
        return False


def main():
    """Función principal de la aplicación"""
    st.set_page_config(page_title="Agente de Historias", layout="centered")
    st.title("📖 Agente Creativo de Historias")

    # Inicializar session_state
    inicializar_session_state()

    # Sección de configuraciones favoritas
    st.sidebar.header("⭐ Configuraciones Favoritas")

    # Guardar configuración actual
    nombre_config = st.sidebar.text_input("Nombre para la configuración:")
    if st.sidebar.button("💾 Guardar Configuración Actual"):
        if nombre_config.strip():
            config_actual = obtener_configuracion_actual()
            success = guardar_configuracion_favorita(
                nombre_config.strip(), config_actual
            )
            if success:
                st.sidebar.success(f"Configuración '{nombre_config}' guardada!")
            else:
                st.sidebar.error("Error al guardar la configuración.")
        else:
            st.sidebar.error("Por favor ingresa un nombre para la configuración.")

    # Cargar configuración favorita
    configuraciones_disponibles = obtener_nombres_configuraciones()
    if configuraciones_disponibles:
        config_seleccionada = st.sidebar.selectbox(
            "Configuraciones guardadas:",
            ["Selecciona una configuración..."] + configuraciones_disponibles,
        )

        if st.sidebar.button("📂 Cargar Configuración"):
            if config_seleccionada != "Selecciona una configuración...":
                if cargar_configuracion_favorita(config_seleccionada):
                    st.sidebar.success(
                        f"Configuración '{config_seleccionada}' cargada!"
                    )
                    st.rerun()
                else:
                    st.sidebar.error("Error al cargar la configuración.")
            else:
                st.sidebar.error("Por favor selecciona una configuración.")

        # Eliminar configuración
        if st.sidebar.button("🗑️ Eliminar Configuración"):
            if config_seleccionada != "Selecciona una configuración...":
                success = eliminar_configuracion_favorita(config_seleccionada)
                if success:
                    st.sidebar.success(
                        f"Configuración '{config_seleccionada}' eliminada!"
                    )
                    st.rerun()
                else:
                    st.sidebar.error("Error al eliminar la configuración.")
    else:
        st.sidebar.info("No hay configuraciones guardadas aún.")

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
            "🔓 Resolución esperada",
            value=st.session_state.entrada.get("resolucion", ""),
        )
        longitud = st.radio(
            "📏 Longitud deseada",
            list(LENGTH_OPTIONS.keys()),
            index=list(LENGTH_OPTIONS.keys()).index(
                st.session_state.entrada.get("longitud", "Mediana")
            ),
        )
        dialogo = st.checkbox(
            "💬 Incluir diálogos entre personajes",
            value=st.session_state.entrada.get("incluir_dialogo", False),
        )

        submitted = st.form_submit_button("Generar Historia")

    # Procesar envío del formulario
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
            "incluir_dialogo": dialogo,
        }

        # Actualizar session_state con los datos actuales
        st.session_state.entrada = {
            "personajes": personajes,
            "escenario": escenario,
            "género": genero,
            "tono": tono,
            "conflicto": conflicto,
            "obstaculos": obstaculos,
            "resolucion": resolucion,
            "longitud": longitud,
            "incluir_dialogo": dialogo,
        }

        es_valida, mensaje = validar_entrada(entrada)

        if not es_valida:
            st.error(mensaje)
        else:
            st.session_state.generando = True
            with st.spinner("Generando historia..."):
                success = procesar_generacion_historia(entrada)
            st.session_state.generando = False

    # Mostrar historia y opciones de acción
    if st.session_state.historia:
        st.text_area("📚 Historia completa", st.session_state.historia, height=400)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Descargar Historia",
                data=st.session_state.historia,
                file_name="historia_generada.txt",
                mime="text/plain",
                disabled=st.session_state.generando,
            )
        with col2:
            continuar = st.button(
                "📎 Continuar Historia",
                disabled=st.session_state.generando,
                key="btn_continuar",
            )

        if not st.session_state.generando and continuar:
            st.session_state.generando = True
            with st.spinner("Generando continuación..."):
                success = procesar_continuacion_historia()
                st.rerun()
            st.session_state.generando = False


if __name__ == "__main__":
    main()
