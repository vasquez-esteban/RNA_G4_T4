"""Funciones auxiliares para filtrado de contenido generado por LLMs"""

import re

# Palabras prohibidas tomadas de
# https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words
# Este diccionario es extensible y adaptable según necesidades

PALABRAS_PROHIBIDAS = {
    "asesinato",
    "asno",
    "bastardo",
    "bollera",
    "cabrón",
    "caca",
    "chupada",
    "chupapollas",
    "chupetón",
    "concha",
    "concha de tu madre",
    "coño",
    "coprofagía",
    "culo",
    "drogas",
    "esperma",
    "fiesta de salchichas",
    "follador",
    "follar",
    "gilipichis",
    "gilipollas",
    "hacer una paja",
    "haciendo el amor",
    "heroína",
    "hija de puta",
    "hijaputa",
    "hijo de puta",
    "hijoputa",
    "idiota",
    "imbécil",
    "infierno",
    "jilipollas",
    "kapullo",
    "lameculos",
    "maciza",
    "macizorra",
    "maldito",
    "mamada",
    "marica",
    "maricón",
    "mariconazo",
    "martillo",
    "mierda",
    "nazi",
    "orina",
    "pedo",
    "pendejo",
    "pervertido",
    "pezón",
    "pinche",
    "pis",
    "prostituta",
    "puta",
    "racista",
    "ramera",
    "sádico",
    "semen",
    "sexo",
    "sexo oral",
    "soplagaitas",
    "soplapollas",
    "tetas grandes",
    "tía buena",
    "travesti",
    "trio",
    "verga",
    "vete a la mierda",
    "vulva",
}


def contiene_contenido_sensible(texto: str) -> bool:
    """
    Evalúa si el texto contiene palabras sensibles usando coincidencias exactas
    """
    texto_normalizado = texto.lower()

    # Usar límites de palabra para evitar falsos positivos
    for palabra in PALABRAS_PROHIBIDAS:
        patron = r"\b" + re.escape(palabra) + r"\b"
        if re.search(patron, texto_normalizado):
            return True
    return False
