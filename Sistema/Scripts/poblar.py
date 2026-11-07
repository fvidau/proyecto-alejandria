"""
Poblado del vault Proyecto Alejandría desde la Biblioteca.

Uso (desde la carpeta del vault):
    python "00 Sistema/Scripts/poblar.py"            # crea notas nuevas y completa campos vacíos
    python "00 Sistema/Scripts/poblar.py" --simular  # muestra qué haría, sin escribir

Reglas (ver 00 Sistema/Diseño del vault.md §6.1):
- Nunca pisa metadatos ni cuerpo de notas existentes: solo crea notas nuevas
  y completa campos que estén vacíos.
- Nunca toca los archivos de la Biblioteca.
"""
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
VAULT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent


def _ruta_biblioteca():
    """La ruta de la Biblioteca vive en config.local.json (no se publica)."""
    import json
    import os
    cfg = SCRIPTS / "config.local.json"
    if cfg.exists():
        return Path(json.loads(cfg.read_text(encoding="utf-8"))["biblioteca"])
    if os.environ.get("ALEJANDRIA_BIBLIOTECA"):
        return Path(os.environ["ALEJANDRIA_BIBLIOTECA"])
    sys.exit("Falta la ruta de la Biblioteca: copiá config.ejemplo.json como "
             "config.local.json y completala.")


BIBLIOTECA = _ruta_biblioteca()
PLANTILLAS = VAULT / "00 Sistema" / "Plantillas"
DIR_AUTORES = VAULT / "10 Biblioteca" / "Autores"
DIR_OBRAS = VAULT / "10 Biblioteca" / "Obras"
DIR_TRADICIONES = VAULT / "10 Biblioteca" / "Tradiciones"
DIR_REPORTES = VAULT / "00 Sistema" / "Reportes"

EXTENSIONES = {".pdf", ".doc", ".docx", ".odt", ".txt", ".epub"}
EXCLUIR = {"Automate the Boring Stuff with Python"}

EXO, ESO, PUENTE = "exoterica", "esoterica", "puente"

# Carpeta física -> (tradición, ala, área)
CARPETAS = {
    "Ciencia/Antropología y Sociología": ("Antropología y Sociología", EXO, "Ciencia"),
    "Ciencia/Ciencias Naturales y Física": ("Ciencias Naturales y Física", EXO, "Ciencia"),
    "Ciencia/Educación": ("Educación", EXO, "Ciencia"),
    "Ciencia/Otros": ("Ciencias (otras)", EXO, "Ciencia"),
    "Ciencia/Psicología y Psicoanálisis": ("Psicología y Psicoanálisis", EXO, "Ciencia"),
    "Filosofía": ("Filosofía Moderna", EXO, "Filosofía"),
    "Filosofía/Existencialismo y Fenomenología": ("Existencialismo y Fenomenología", EXO, "Filosofía"),
    "Filosofía/Filosofía Antigua": ("Filosofía Antigua", EXO, "Filosofía"),
    "Filosofía/Filosofía Argentina": ("Filosofía Argentina", EXO, "Filosofía"),
    "Filosofía/Filosofía Contemporánea": ("Filosofía Contemporánea", EXO, "Filosofía"),
    "Filosofía/Filosofía Medieval y Renacentista": ("Filosofía Medieval y Renacentista", EXO, "Filosofía"),
    "Filosofía/Filosofía Moderna": ("Filosofía Moderna", EXO, "Filosofía"),
    "Filosofía/Filosofía Política": ("Filosofía Política", EXO, "Filosofía"),
    "Filosofía/Idealismo y Romanticismo": ("Filosofía del Siglo XIX", EXO, "Filosofía"),
    "Historia/Historia Antigua": ("Historia Antigua", EXO, "Historia"),
    "Historia/Historia Argentina": ("Historia Argentina", EXO, "Historia"),
    "Historia/Historia Contemporánea": ("Historia Contemporánea", EXO, "Historia"),
    "Historia/Historia de las Ideas": ("Historia de las Ideas", EXO, "Historia"),
    "Historia/Historia Medieval y Moderna": ("Historia Medieval y Moderna", EXO, "Historia"),
    "Literatura/Literatura Argentina": ("Literatura Argentina", EXO, "Literatura"),
    "Literatura/Literatura del Siglo XIX": ("Literatura del Siglo XIX", EXO, "Literatura"),
    "Literatura/Literatura del Siglo XX": ("Literatura del Siglo XX", EXO, "Literatura"),
    "Literatura/Literatura Grecolatina": ("Literatura Grecolatina", EXO, "Literatura"),
    "Literatura/Literatura Latinoamericana": ("Literatura Latinoamericana", EXO, "Literatura"),
    "Literatura/Literatura Medieval y Renacentista": ("Literatura Medieval y Renacentista", EXO, "Literatura"),
    "Literatura/Literatura Oriental": ("Literatura Oriental", EXO, "Literatura"),
    "Literatura/Poesía": ("Poesía", EXO, "Literatura"),
    "Ocultismo y Esoterismo/Antroposofía": ("Antroposofía", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Cábala": ("Cábala", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Chamanismo y Nagualismo": ("Chamanismo y Nagualismo", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Cuarto Camino": ("Cuarto Camino", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Gnosticismo y Mística Cristiana": ("Gnosticismo y Mística Cristiana", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Hermetismo y Alquimia": ("Hermetismo y Alquimia", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Islam Esotérico": ("Islam Esotérico", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Magia Ceremonial": ("Magia Ceremonial", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Mitología y Simbolismo": ("Mitología y Simbolismo", PUENTE, "Puente"),
    "Ocultismo y Esoterismo/Teosofía": ("Teosofía", ESO, "Esoterismo"),
    "Ocultismo y Esoterismo/Yoga, Vedanta y Misticismo Oriental": ("Yoga, Vedanta y Misticismo Oriental", ESO, "Esoterismo"),
    "Textos Sagrados": ("Textos Sagrados", PUENTE, "Puente"),
}

# Tradiciones nuevas (no existen como carpeta) -> (ala, área)
TRADICIONES_NUEVAS = {
    "Economía Política": (EXO, "Filosofía"),
    "Arte, Estética y Crítica": (EXO, "Arte"),
    "Pensamiento Oriental": (EXO, "Filosofía"),
    "Religión y Teología": (EXO, "Historia"),
    "Historia de las Religiones": (EXO, "Historia"),
    "Lingüística": (EXO, "Ciencia"),
    "Literatura de los Siglos XVII–XVIII": (EXO, "Literatura"),
    "Literatura del Antiguo Oriente": (EXO, "Literatura"),
    "Biografía y Memorias": (EXO, "Literatura"),
    "Tradicionalismo": (ESO, "Esoterismo"),
    "Rosacrucismo": (ESO, "Esoterismo"),
    "Masonería": (ESO, "Esoterismo"),
    "Tarot": (ESO, "Esoterismo"),
    "Nuevo Pensamiento y Nueva Era": (ESO, "Esoterismo"),
    "Budismo": (ESO, "Esoterismo"),
    "Martinismo": (ESO, "Esoterismo"),
    "Pitagorismo": (ESO, "Esoterismo"),
}

# Archivos sin "Autor - Título" o con autor mal puesto: base -> (autor crudo o None, título)
ESPECIALES = {
    "De la seducción": ("Jean Baudrillard", "De la seducción"),
    "Voz del Silencio": ("Blavatsky", "La Voz del Silencio"),
    "La Joya del Discernimiento": ("Sankaracharya", "La joya del discernimiento"),
    "La Tabla de Esmeralda Hortulano Fulcanelli Hermes Trismegistos": ("Trismegisto", "La Tabla de Esmeralda (Hortulano, Fulcanelli)"),
    "LIBER B VEL MAGI SVB FIGVRÂ I": ("Crowley", "Liber B vel Magi"),
    "LIBER TZADDI VEL HAMVS HERMETICVS SVB FIGVRÂ XC": ("Crowley", "Liber Tzaddi vel Hamus Hermeticus"),
    "San Agustin de Hipona  La ciudad de Dios": ("San Agustin de Hipona", "La ciudad de Dios"),
    "Numenio - Oraculos caldeos": (None, "Oráculos caldeos"),
    "Pericles - Discurso funebre (Tucidides)": ("Tucidides", "Discurso fúnebre de Pericles"),
    "Cantar de los Nivelungos": (None, "Cantar de los Nibelungos"),
    "Aristóteles - Ética a Nicómano": ("Aristóteles", "Ética a Nicómaco"),
}

# Tradición por defecto para obras sueltas en la raíz de "Ocultismo y Esoterismo"
RAIZ_OCULTISMO_POR_AUTOR = {
    "René Guénon": "Tradicionalismo",
    "Julius Evola": "Tradicionalismo",
    "Aldous Huxley": "Tradicionalismo",
    "Rudolf Steiner": "Antroposofía",
    "Helena Blavatsky": "Teosofía",
    "Sri Aurobindo": "Yoga, Vedanta y Misticismo Oriental",
    "Paul Brunton": "Yoga, Vedanta y Misticismo Oriental",
    "Paramahansa Yogananda": "Yoga, Vedanta y Misticismo Oriental",
}

# Reclasificaciones por obra (de "Revisión de clasificación").
# Se aplican todas las que coinciden, en orden. Coincidencia: subcadena del
# nombre de archivo, sin tildes y en minúsculas.
#   t: reemplaza tradiciones · pc: suma puente_con · e: suma etiquetas
#   propia: la obra no hereda del autor
O = [
    # Raíz de la Biblioteca
    ("coomaraswamy", dict(t=["Tradicionalismo"], pc=["Arte, Estética y Crítica"])),
    ("infocracia", dict(t=["Filosofía Contemporánea"])),
    ("respuesta a job", dict(t=["Psicología y Psicoanálisis"], pc=["Gnosticismo y Mística Cristiana"])),
    ("de la seduccion", dict(t=["Filosofía Contemporánea"])),
    ("la ilusion vital", dict(t=["Filosofía Contemporánea"])),
    ("el yoga tantrico", dict(t=["Tradicionalismo"])),
    ("marco aurelio - meditaciones", dict(t=["Filosofía Antigua"])),
    ("mentalidad de la edad de bronce", dict(t=["Historia Antigua"], e=["revisar"])),
    ("in search of the miraculous", dict(t=["Cuarto Camino"])),
    ("ouspensky - la vida de ivan osokin", dict(t=["Cuarto Camino"])),
    ("voz del silencio", dict(t=["Teosofía"])),
    # Ocultismo raíz: textos políticos de Evola
    ("fascismo desde la derecha", dict(t=["Filosofía Política"], propia=True)),
    ("los hombres y las ruinas", dict(t=["Filosofía Política"], propia=True)),
    ("la doctrina del despertar", dict(t=["Tradicionalismo", "Budismo"])),
    # Filosofía
    ("chesterton - el hombre comun", dict(t=["Filosofía Contemporánea"])),
    ("chesterton - el hombre eterno", dict(t=["Filosofía Contemporánea"])),
    ("chesterton - ortodoxia", dict(t=["Filosofía Contemporánea"])),
    ("no toda es vigilia", dict(t=["Filosofía Argentina"])),
    ("musil - sobre la estupidez", dict(t=["Filosofía Contemporánea"])),
    ("blanchot", dict(t=["Arte, Estética y Crítica"])),
    ("simone weil", dict(t=["Filosofía Contemporánea"])),
    ("oraculos caldeos", dict(t=["Filosofía Antigua"], pc=["Hermetismo y Alquimia"], e=["neoplatonismo"])),
    ("confusio", dict(t=["Pensamiento Oriental"])),
    ("sun tzu", dict(t=["Pensamiento Oriental"])),
    ("bacon - ", dict(t=["Filosofía Moderna"])),
    ("nueva atlantida", dict(pc=["Rosacrucismo"])),
    ("spencer - primeros principios", dict(t=["Filosofía del Siglo XIX"])),
    ("wilde - el critico artista", dict(t=["Arte, Estética y Crítica"])),
    ("wilde - la decadencia de la mentira", dict(t=["Arte, Estética y Crítica"])),
    ("ayn rand - el manifiesto romantico", dict(t=["Arte, Estética y Crítica"])),
    ("smith - la riqueza", dict(t=["Economía Política"])),
    ("menger - ", dict(t=["Economía Política"])),
    ("von mises - ", dict(t=["Economía Política"])),
    ("hazlitt - ", dict(t=["Economía Política"])),
    ("kirzner - ", dict(t=["Economía Política"])),
    ("huerta de soto", dict(t=["Economía Política"])),
    ("rothbard - hombre, economia", dict(t=["Economía Política"])),
    ("bastiat - ", dict(t=["Economía Política"])),
    ("stuart mill - principios de economia", dict(t=["Economía Política"])),
    ("de molinari", dict(t=["Economía Política"])),
    ("mankiw", dict(t=["Economía Política"])),
    ("canetti - masa y poder", dict(t=["Antropología y Sociología"])),
    ("weber - la etica protestante", dict(t=["Antropología y Sociología"])),
    ("sontag - ", dict(t=["Arte, Estética y Crítica"])),
    ("gaarder", dict(t=["Literatura del Siglo XX"])),
    ("peterson - 12 reglas", dict(t=["Psicología y Psicoanálisis"])),
    ("lewkowicz - pensar sin estado", dict(t=["Filosofía Argentina"])),
    ("mujica - ensayos", dict(t=["Filosofía Argentina"])),
    ("alberdi - fragmento preliminar", dict(t=["Filosofía Argentina"])),
    ("alberdi - la omnipotencia", dict(t=["Filosofía Argentina"])),
    ("castellani - la desintegracion", dict(t=["Filosofía Argentina"])),
    # Ciencia
    ("kuhne - ", dict(t=["Ciencias (otras)"])),
    ("barba - antropologia teatral", dict(t=["Arte, Estética y Crítica"])),
    ("morin - el cine", dict(t=["Arte, Estética y Crítica"])),
    ("saussure", dict(t=["Lingüística"])),
    ("jacques vallee", dict(e=["fenomenos-anomalos"])),
    # Historia
    ("lutero - ", dict(t=["Religión y Teología"])),
    ("calvinus - ", dict(t=["Religión y Teología"])),
    ("loyola - ", dict(t=["Religión y Teología"], pc=["Gnosticismo y Mística Cristiana"])),
    ("kissinger", dict(t=["Historia Contemporánea"])),
    ("browne - hidriotaphia", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("michelet - la bruja", dict(pc=["Magia Ceremonial"])),
    ("tarkovsky", dict(t=["Arte, Estética y Crítica"])),
    ("valery - degas", dict(t=["Arte, Estética y Crítica"])),
    ("harold bloom", dict(t=["Arte, Estética y Crítica"])),
    ("mauclair", dict(t=["Arte, Estética y Crítica"])),
    ("de quincey - los ultimos dias", dict(t=["Literatura del Siglo XIX"])),
    ("renan - vida de jesus", dict(t=["Religión y Teología"])),
    ("diogenes laercio", dict(t=["Historia Antigua", "Filosofía Antigua"])),
    ("saint simon - wikipedia", dict(e=["revisar"])),
    ("babilonia - paper", dict(e=["revisar"])),
    # Literatura
    ("defoe - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("swift - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("voltaire - candido", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("montesquieu - cartas persas", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("mirabeau - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("schiller - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("shiller - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("joven werther", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("moliere - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("milton - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("gongora - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("quevedo - historia de la vida del buscon", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("quevedo - suenos", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("lafontaine - ", dict(t=["Literatura de los Siglos XVII–XVIII"])),
    ("cazzotte", dict(t=["Literatura de los Siglos XVII–XVIII"], pc=["Martinismo"], e=["literatura-ocultista"])),
    ("quevedo - providencia", dict(t=["Religión y Teología"])),
    ("gilgamesh", dict(t=["Literatura del Antiguo Oriente"])),
    ("sinuhe", dict(t=["Literatura del Antiguo Oriente"])),
    ("las mil y una noches", dict(t=["Literatura Oriental"])),
    ("fitzgerlad - rubaiyat", dict(t=["Literatura Oriental"])),
    ("umberto eco - el pendulo", dict(e=["literatura-ocultista"], pc=["Hermetismo y Alquimia"])),
    ("woody allen", dict(t=["Biografía y Memorias"])),
    ("artaud - van gogh", dict(t=["Arte, Estética y Crítica"])),
    ("por que leer los clasicos", dict(t=["Arte, Estética y Crítica"])),
    ("juan carlos gomez", dict(t=["Arte, Estética y Crítica"])),
    ("barba - el teatro", dict(t=["Arte, Estética y Crítica"])),
    # Esotérica
    ("heindel - ", dict(t=["Rosacrucismo"])),
    ("hargrave - ", dict(t=["Rosacrucismo"])),
    ("christian rosacruz", dict(t=["Rosacrucismo"])),
    ("manly palmer hall", dict(t=["Rosacrucismo"])),
    ("hall manly", dict(t=["Rosacrucismo"])),
    ("pike - moral", dict(t=["Masonería"])),
    ("ragon - ", dict(t=["Masonería"])),
    ("reghin - ", dict(t=["Masonería"])),
    ("papus - el tarot", dict(t=["Tarot"])),
    ("sallie - jung y el tarot", dict(t=["Tarot"])),
    ("atkinson - ", dict(t=["Nuevo Pensamiento y Nueva Era"])),
    ("guy ballard", dict(t=["Nuevo Pensamiento y Nueva Era"])),
    ("saint germain - el libro de oro", dict(t=["Nuevo Pensamiento y Nueva Era"])),
    ("mendez - la voz", dict(t=["Nuevo Pensamiento y Nueva Era"])),
    ("saint germain - santisima trinosofia", dict(t=["Hermetismo y Alquimia"])),
    ("hartmann - ", dict(t=["Teosofía"])),
    ("prasad - ", dict(t=["Teosofía"])),
    ("stanislas de guaita", dict(t=["Martinismo"])),
    ("lois claude de san matin", dict(t=["Martinismo"])),
    ("fortune - la sacerdotisa", dict(e=["literatura-ocultista"])),
    ("crowley - el testamento de magdalen", dict(e=["literatura-ocultista"])),
    ("crowley - la estratagema", dict(e=["literatura-ocultista"])),
    ("bulwer-lytton - zanoni", dict(t=["Literatura del Siglo XIX"], pc=["Hermetismo y Alquimia"], e=["literatura-ocultista"], propia=True)),
    ("bulwer-lytton - la raza futura", dict(t=["Literatura del Siglo XIX"], pc=["Hermetismo y Alquimia"], e=["literatura-ocultista"], propia=True)),
    ("blake - all religions", dict(t=["Poesía"], pc=["Hermetismo y Alquimia"])),
    ("boehme - ", dict(t=["Gnosticismo y Mística Cristiana"])),
    ("boheme - ", dict(t=["Gnosticismo y Mística Cristiana"])),
    ("jung - el secreto de la flor de oro", dict(t=["Yoga, Vedanta y Misticismo Oriental"])),
    ("fabre-d", dict(t=["Pitagorismo"])),
    ("filostrato - ", dict(t=["Pitagorismo"])),
    ("de nerval - aurelia", dict(t=["Literatura del Siglo XIX"], pc=["Gnosticismo y Mística Cristiana"], e=["literatura-ocultista"], propia=True)),
    ("castellani - el apocalipsis", dict(t=["Religión y Teología"])),
    ("eliade - ", dict(t=["Historia de las Religiones"], pc=["Mitología y Simbolismo"])),
    ("cambell - ", dict(t=["Historia de las Religiones"], pc=["Mitología y Simbolismo"])),
    ("libro de los muertos", dict(t=["Textos Sagrados"])),
    ("libro egipcio de los muertos", dict(t=["Textos Sagrados"])),
    ("gershom - ", dict(e=["estudio-academico"])),
    ("alexandra david neel", dict(t=["Budismo"])),
    ("collins - el idilio", dict(e=["literatura-ocultista"])),
    ("san alfonso maria de ligorio", dict(t=["Gnosticismo y Mística Cristiana"])),
    ("mahabharata", dict(t=["Textos Sagrados", "Literatura Oriental"])),
    ("valmiki - ramayana", dict(t=["Textos Sagrados", "Literatura Oriental"])),
    ("sutra del diamante", dict(t=["Textos Sagrados", "Budismo"])),
]

# Cruces y etiquetas a nivel autor (se heredan a sus obras salvo clasificacion_propia)
AUTOR_EXTRA = {
    "Plotino": dict(pc=["Hermetismo y Alquimia"], e=["neoplatonismo"]),
    "Proclo": dict(pc=["Hermetismo y Alquimia"], e=["neoplatonismo"]),
    "Jámblico": dict(pc=["Hermetismo y Alquimia", "Pitagorismo"], e=["neoplatonismo"]),
    "Porfirio": dict(pc=["Hermetismo y Alquimia", "Pitagorismo"], e=["neoplatonismo"]),
    "Numenio de Apamea": dict(pc=["Hermetismo y Alquimia"], e=["neoplatonismo"]),
    "Pitágoras": dict(pc=["Pitagorismo"]),
    "Filón de Alejandría": dict(pc=["Hermetismo y Alquimia", "Cábala"]),
    "Clemente de Alejandría": dict(pc=["Gnosticismo y Mística Cristiana"]),
    "Nicolás de Cusa": dict(pc=["Gnosticismo y Mística Cristiana"], e=["mistica"]),
    "Simone Weil": dict(pc=["Gnosticismo y Mística Cristiana"], e=["mistica"]),
    "Hugo Mujica": dict(pc=["Gnosticismo y Mística Cristiana"], e=["mistica"]),
    "Ralph Waldo Emerson": dict(pc=["Yoga, Vedanta y Misticismo Oriental"], e=["trascendentalismo"]),
    "Thomas Carlyle": dict(e=["trascendentalismo"]),
    "Carl Gustav Jung": dict(pc=["Hermetismo y Alquimia", "Mitología y Simbolismo"]),
    "Fritjof Capra": dict(pc=["Yoga, Vedanta y Misticismo Oriental"]),
    "Rumi": dict(pc=["Islam Esotérico"], e=["sufismo"]),
    "Hafiz": dict(pc=["Islam Esotérico"], e=["sufismo"]),
    "Saadi de Shiraz": dict(pc=["Islam Esotérico"], e=["sufismo"]),
    "Abu al-Husayn al-Nuri": dict(e=["sufismo"]),
    "Gustav Meyrink": dict(pc=["Hermetismo y Alquimia", "Cábala"], e=["literatura-ocultista"]),
    "H. P. Lovecraft": dict(e=["literatura-ocultista"]),
    "Algernon Blackwood": dict(e=["literatura-ocultista"]),
    "Fernando Pessoa": dict(pc=["Rosacrucismo"], e=["literatura-ocultista"]),
    "Giordano Bruno": dict(pc=["Filosofía Medieval y Renacentista"]),
    "Marsilio Ficino": dict(pc=["Filosofía Medieval y Renacentista"], e=["neoplatonismo"]),
    "William Blake": dict(pc=["Hermetismo y Alquimia"]),
    "Ananda K. Coomaraswamy": dict(e=["perennialismo"]),
    "Aldous Huxley": dict(e=["perennialismo"]),
    "René Guénon": dict(e=["perennialismo"]),
    "Gershom Scholem": dict(e=["estudio-academico"]),
    "Titus Burckhardt": dict(e=["perennialismo"]),
}

HOY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def nfc(s):
    return unicodedata.normalize("NFC", s)


def plano(s):
    """minúsculas sin tildes, para comparar."""
    s = unicodedata.normalize("NFD", nfc(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("’", "'")


SUFIJOS = [
    r"-desktop-\w+$", r"\s*-\s*ebook$", r"\s*\(ebook\)$", r"\s*-\s*epub$", r"\s*-\s*e$",
    r"\s*\(\d\)$", r"\s*-\s*$", r"\s*-\s*\d{4}$", r"\s*\(\d{4}\)$", r"\s*-\s*\(?\d{4}\)?$",
]


def limpiar_titulo(t):
    t = nfc(t).strip()
    cambio = True
    while cambio:
        cambio = False
        for p in SUFIJOS:
            nuevo = re.sub(p, "", t, flags=re.I).strip()
            if nuevo != t:
                t, cambio = nuevo, True
    return re.sub(r"\s{2,}", " ", t)


def clave_titulo(t):
    return re.sub(r"[^a-z0-9]+", " ", plano(limpiar_titulo(t))).strip()


def nombre_archivo(s, largo=120):
    s = re.sub(r'[\\/:*?"<>|#^\[\]]', "", nfc(s)).strip().rstrip(".")
    return s[:largo].strip()


def link(n):
    return f"[[{n}]]"


def yaml_valor(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None or v == "":
        return ""
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(yaml_valor_str(x) for x in v) + "]"
    return yaml_valor_str(v)


def yaml_valor_str(x):
    return '"' + str(x).replace("\\", "\\\\").replace('"', '\\"') + '"'


def frontmatter(campos):
    lineas = ["---"]
    for k, v in campos.items():
        val = yaml_valor(v)
        lineas.append(f"{k}: {val}" if val != "" else f"{k}:")
    lineas.append("---")
    return "\n".join(lineas)


def cuerpo_plantilla(nombre, titulo):
    txt = (PLANTILLAS / nombre).read_text(encoding="utf-8")
    partes = txt.split("---", 2)
    cuerpo = partes[2] if len(partes) == 3 else txt
    return cuerpo.replace("{{title}}", titulo).lstrip("\n")


def escribir(ruta, campos, cuerpo, simular, stats, tipo):
    """Crea la nota o, si existe, solo completa campos vacíos del frontmatter."""
    if not ruta.exists():
        stats[f"{tipo}: creadas"] += 1
        if not simular:
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.write_text(frontmatter(campos) + "\n\n" + cuerpo, encoding="utf-8")
        return
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    if not m:
        stats[f"{tipo}: sin frontmatter (no tocadas)"] += 1
        return
    lineas = m.group(1).split("\n")
    presentes = {}
    for i, l in enumerate(lineas):
        mm = re.match(r"^([a-z_]+):\s*(.*)$", l)
        if mm:
            presentes[mm.group(1)] = (i, mm.group(2).strip())
    cambios = 0
    for k, v in campos.items():
        nuevo = yaml_valor(v)
        if nuevo in ("", "[]"):
            continue
        if k not in presentes:
            lineas.append(f"{k}: {nuevo}")
            cambios += 1
        else:
            i, actual = presentes[k]
            if actual in ("", "[]", '""'):
                lineas[i] = f"{k}: {nuevo}"
                cambios += 1
    if cambios:
        stats[f"{tipo}: completadas"] += 1
        if not simular:
            ruta.write_text("---\n" + "\n".join(lineas) + "\n---\n" + texto[m.end():], encoding="utf-8")
    else:
        stats[f"{tipo}: sin cambios"] += 1


def unir(*listas):
    out = []
    for l in listas:
        for x in l or []:
            if x not in out:
                out.append(x)
    return out


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
def cargar_autores():
    tabla = {}
    with open(SCRIPTS / "autores.csv", encoding="utf-8") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            nombres = [n for n in fila["nombre"].split("|")] if fila["nombre"] else []
            def parte(campo, i):
                vals = (fila[campo] or "").split("|")
                return vals[i] if i < len(vals) else ""
            personas = []
            for i, n in enumerate(nombres):
                if not n:
                    continue
                personas.append(dict(
                    nombre=nfc(n.strip()),
                    nacimiento=int(parte("nacimiento", i)) if parte("nacimiento", i).strip() else None,
                    muerte=int(parte("muerte", i)) if parte("muerte", i).strip() else None,
                    origen=parte("origen", i).strip(),
                ))
            tabla[plano(fila["raw"])] = personas
    return tabla


def tradicion_info(nombre):
    for (t, ala, area) in CARPETAS.values():
        if t == nombre:
            return ala, area
    if nombre in TRADICIONES_NUEVAS:
        return TRADICIONES_NUEVAS[nombre]
    raise KeyError(f"Tradición desconocida: {nombre}")


def main():
    simular = "--simular" in sys.argv
    autores_tabla = cargar_autores()
    stats = Counter()
    avisos = defaultdict(list)

    # 1. Leer la Biblioteca
    obras = {}  # clave -> dict
    for f in sorted(BIBLIOTECA.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in EXTENSIONES:
            continue
        rel = f.relative_to(BIBLIOTECA)
        if rel.parts[0] == "Indice":
            continue
        base = nfc(f.stem)
        if base in EXCLUIR:
            avisos["Excluidos (no son del proyecto)"].append(str(rel))
            continue

        base_limpia = limpiar_titulo(base)
        if base_limpia in ESPECIALES or base in ESPECIALES:
            raw, titulo = ESPECIALES.get(base_limpia) or ESPECIALES[base]
        else:
            m = re.match(r"^(.+?)\s+-\s*(.+)$", base)
            raw, titulo = (m.group(1).strip(), m.group(2).strip()) if m else (None, base)

        personas = []
        if raw:
            personas = autores_tabla.get(plano(raw))
            if personas is None:
                avisos["Autores no encontrados en autores.csv"].append(f"{raw} ← {rel}")
                personas = [dict(nombre=nfc(raw), nacimiento=None, muerte=None, origen="")]
            if not personas:  # autor vacío en la tabla = obra anónima / tradicional
                titulo = base
        titulo = limpiar_titulo(titulo)
        nombres = [p["nombre"] for p in personas]

        # clasificación por carpeta
        carpeta = "/".join(rel.parts[:-1])
        if carpeta in CARPETAS:
            trad, ala, _ = CARPETAS[carpeta]
            trads = [trad]
        elif carpeta == "Ocultismo y Esoterismo":
            trads = [RAIZ_OCULTISMO_POR_AUTOR.get(nombres[0] if nombres else "", "")]
        else:
            trads = []
        pc, etq, propia = [], [], False
        p = plano(base)
        for patron, cambio in O:
            if patron in p:
                if "t" in cambio:
                    trads = list(cambio["t"])
                pc = unir(pc, cambio.get("pc"))
                etq = unir(etq, cambio.get("e"))
                propia = propia or cambio.get("propia", False)
        trads = [t for t in trads if t]
        if not trads:
            avisos["Obras sin tradición (revisar)"].append(str(rel))
        alas = [tradicion_info(t)[0] for t in trads]
        ala = next((a for a in alas if a != PUENTE), alas[0] if alas else "")

        clave = (tuple(nombres), clave_titulo(titulo))
        archivo = rel.as_posix()
        if clave in obras:
            o = obras[clave]
            # preferir la copia clasificada (no en la raíz) y el nombre más corto
            actual_raiz = "/" not in o["archivo"]
            if actual_raiz and "/" in archivo:
                o["duplicados"].append(o["archivo"])
                o.update(archivo=archivo, tradiciones=trads, ala=ala, puente_con=pc, etiquetas=etq, propia=propia)
            else:
                o["duplicados"].append(archivo)
            continue
        obras[clave] = dict(
            personas=personas, titulo=titulo, archivo=archivo, formato=f.suffix.lower().lstrip("."),
            tradiciones=trads, ala=ala, puente_con=pc, etiquetas=etq, propia=propia, duplicados=[],
        )

    # 2. Autores: unir clasificación de sus obras
    autores = {}
    for o in obras.values():
        for pers in o["personas"]:
            a = autores.setdefault(pers["nombre"], dict(datos=pers, obras=[], alas=Counter(), trads=[]))
            a["obras"].append(o)
            if not o["propia"]:
                if o["ala"]:
                    a["alas"][o["ala"]] += 1
                a["trads"] = unir(a["trads"], o["tradiciones"])
    for nombre, a in autores.items():
        extra = AUTOR_EXTRA.get(nombre, {})
        a["puente_con"] = list(extra.get("pc", []))
        a["etiquetas"] = list(extra.get("e", []))
        no_puente = [(n, al) for al, n in a["alas"].items() if al != PUENTE]
        a["ala"] = max(no_puente)[1] if no_puente else (PUENTE if a["alas"] else "")
        # las obras heredan cruces y etiquetas del autor
        for o in a["obras"]:
            if not o["propia"]:
                o["puente_con"] = unir(o["puente_con"], [t for t in a["puente_con"] if t not in o["tradiciones"]])
                o["etiquetas"] = unir(o["etiquetas"], a["etiquetas"])

    # 3. Escribir tradiciones
    usadas = set()
    for o in obras.values():
        usadas.update(o["tradiciones"])
        usadas.update(o["puente_con"])
    mapa = {EXO: "Ala Exotérica", ESO: "Ala Esotérica", PUENTE: "Puentes"}
    for t in sorted(usadas):
        ala, area = tradicion_info(t)
        campos = dict(tipo="tradicion", ala=ala, area=area, padre=link(mapa[ala]))
        escribir(DIR_TRADICIONES / f"{nombre_archivo(t)}.md", campos,
                 cuerpo_plantilla("Plantilla - Tradición.md", t), simular, stats, "Tradiciones")

    # 4. Escribir autores
    for nombre, a in sorted(autores.items()):
        d = a["datos"]
        campos = dict(
            tipo="autor", nombre=nombre, alias=[], ala=a["ala"],
            tradiciones=[link(t) for t in a["trads"]],
            puente_con=[link(t) for t in a["puente_con"]],
            etiquetas=a["etiquetas"],
            nacimiento=d["nacimiento"], muerte=d["muerte"], origen=d["origen"],
            datos_verificados=False, estado="semilla",
        )
        if d["nacimiento"] is None and d["muerte"] is None:
            avisos["Autores sin fechas"].append(nombre)
        escribir(DIR_AUTORES / f"{nombre_archivo(nombre)}.md", campos,
                 cuerpo_plantilla("Plantilla - Autor.md", nombre), simular, stats, "Autores")

    # 5. Escribir obras
    vistos = Counter()
    for o in sorted(obras.values(), key=lambda x: (x["archivo"])):
        nombres = [p["nombre"] for p in o["personas"]]
        autor_txt = " y ".join(nombres)
        nombre_nota = nombre_archivo(f"{autor_txt} - {o['titulo']}" if nombres else o["titulo"])
        vistos[nombre_nota] += 1
        if vistos[nombre_nota] > 1:
            nombre_nota = f"{nombre_nota} ({vistos[nombre_nota]})"
            avisos["Nombres repetidos (se numeraron)"].append(nombre_nota)
        if not nombres:
            avisos["Obras anónimas o tradicionales"].append(nombre_nota)
        if o["duplicados"]:
            avisos["Duplicados agrupados en una sola ficha"].append(
                f"{nombre_nota}: " + " · ".join([o["archivo"]] + o["duplicados"]))
        autor_campo = link(nombres[0]) if len(nombres) == 1 else [link(n) for n in nombres]
        campos = dict(
            tipo="obra", titulo=o["titulo"], autor=autor_campo if nombres else "",
            ala=o["ala"], tradiciones=[link(t) for t in o["tradiciones"]],
            puente_con=[link(t) for t in o["puente_con"]], etiquetas=o["etiquetas"],
            clasificacion_propia=o["propia"], archivo=o["archivo"], formato=o["formato"],
            traductor="", dominio_publico="sin-verificar", lectura="sin-leer", prioridad="media",
            duplicados=o["duplicados"], usada_en=[],
        )
        url = "file:///" + quote((BIBLIOTECA / o["archivo"]).as_posix(), safe="/:")
        cuerpo = f"📖 [Abrir archivo]({url})\n\n" + cuerpo_plantilla("Plantilla - Obra.md", nombre_nota)
        escribir(DIR_OBRAS / f"{nombre_nota}.md", campos, cuerpo, simular, stats, "Obras")

    # 6. Reporte
    lineas = [f"# Reporte de poblado — {HOY}", "",
              f"Modo: {'simulación' if simular else 'escritura'}", "",
              "## Resumen", ""]
    lineas += [f"- {k}: {v}" for k, v in sorted(stats.items())]
    lineas += [f"- Obras únicas: {len(obras)}", f"- Autores: {len(autores)}", ""]
    for titulo, items in avisos.items():
        lineas += [f"## {titulo} ({len(items)})", ""] + [f"- {x}" for x in sorted(items)] + [""]
    reporte = "\n".join(lineas)
    if not simular:
        DIR_REPORTES.mkdir(parents=True, exist_ok=True)
        (DIR_REPORTES / f"Poblado {HOY}.md").write_text(reporte, encoding="utf-8")
    print(reporte)


if __name__ == "__main__":
    main()
