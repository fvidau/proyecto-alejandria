"""
Exporta la parte pública del vault Proyecto Alejandría a un repositorio aparte.

Uso (desde la carpeta del vault):
    python "00 Sistema/Scripts/exportar.py"            # genera la copia pública
    python "00 Sistema/Scripts/exportar.py" --simular  # solo muestra qué haría

Qué se publica:
- Autores: metadatos (fechas, origen, ala, tradiciones, cruces) y sus secciones
  de texto cuando estén escritas.
- Obras: solo catálogo (título, autor, clasificación). Nunca la ruta del archivo,
  los duplicados ni el contenido destilado (resumen, ideas, citas).
- Tradiciones: texto curatorial cuando exista, más la lista de autores y obras.
- Sistema: plantillas, vistas, scripts y documentación, sin rutas locales.

La carpeta de salida se define en config.local.json ("salida_publica").
El script solo reescribe las carpetas que él mismo genera (Biblioteca/, Sistema/
y README.md); nunca toca .git ni otros archivos del repositorio.
"""
import json
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

SCRIPTS = Path(__file__).resolve().parent
VAULT = SCRIPTS.parents[1]
SISTEMA = VAULT / "00 Sistema"
BIB = VAULT / "10 Biblioteca"

# Campos que se publican por tipo de nota (todo lo demás queda privado)
CAMPOS_AUTOR = ["nombre", "alias", "ala", "tradiciones", "puente_con", "etiquetas",
                "nacimiento", "muerte", "origen", "datos_verificados"]
CAMPOS_OBRA = ["titulo", "autor", "ala", "tradiciones", "puente_con", "etiquetas",
               "dominio_publico", "lectura"]
SECCIONES_AUTOR = ["Quién fue", "Por qué importa para Alejandría", "Conexiones"]
SECCIONES_TRADICION = ["Qué es", "Por dónde empezar"]
SECCIONES_OBRA = []  # el contenido destilado de las obras no se publica

# Archivos de sistema que se copian (relativos a "00 Sistema")
SISTEMA_PUBLICO = ["CLAUDE.md", "Diseño del vault.md", "Plantillas", "Bases",
                   "Scripts/poblar.py", "Scripts/exportar.py", "Scripts/autores.csv",
                   "Scripts/config.ejemplo.json"]

MARCA = ".alejandria-export"
ALAS = {"exoterica": "Exotérica", "esoterica": "Esotérica", "puente": "Puente"}
LECTURA = {"sin-leer": "Sin destilar", "destilada": "Destilada", "en-curso": "En curso"}


# ---------------------------------------------------------------------------
# Lectura de notas
# ---------------------------------------------------------------------------
def leer_valor(txt):
    txt = txt.strip()
    if txt == "":
        return None
    if txt in ("true", "false"):
        return txt == "true"
    if re.fullmatch(r"-?\d+", txt):
        return int(txt)
    if txt[0] in "[\"":
        try:
            return json.loads(txt)
        except ValueError:
            pass
    if txt[0] == "'" and txt[-1] == "'":
        return txt[1:-1]
    return txt


def leer_nota(ruta):
    texto = ruta.read_text(encoding="utf-8")
    meta, cuerpo = {}, texto
    m = re.match(r"---\n(.*?)\n---\n?(.*)", texto, re.S)
    if m:
        cuerpo = m.group(2)
        clave = None
        for linea in m.group(1).splitlines():
            lista = re.match(r"\s+-\s*(.*)", linea)
            if lista and clave:  # lista en bloque (formato que usa Obsidian al editar)
                if not isinstance(meta.get(clave), list):
                    meta[clave] = []
                meta[clave].append(leer_valor(lista.group(1)))
                continue
            kv = re.match(r"([\w]+):\s?(.*)", linea)
            if kv:
                clave = kv.group(1)
                meta[clave] = leer_valor(kv.group(2))
    return meta, cuerpo


def secciones(cuerpo, nombres):
    """Devuelve {sección: texto} solo para las secciones con contenido real."""
    cuerpo = re.sub(r"<!--.*?-->", "", cuerpo, flags=re.S)
    cuerpo = re.sub(r"```base.*?```", "", cuerpo, flags=re.S)
    partes = re.split(r"^## +(.+?)\s*$", cuerpo, flags=re.M)
    res = {}
    for i in range(1, len(partes), 2):
        nombre, texto = partes[i], partes[i + 1]
        if nombre not in nombres:
            continue
        lineas = [l for l in texto.strip().splitlines()
                  if l.strip() not in ("", "-", ">", "> — p.", "1.", "—")]
        if lineas:
            res[nombre] = "\n".join(lineas)
    return res


def lista(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def destino(enlace):
    m = re.fullmatch(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", str(enlace).strip())
    if not m:
        return str(enlace), str(enlace)
    return m.group(1).strip(), (m.group(2) or m.group(1)).strip()


# ---------------------------------------------------------------------------
# Escritura
# ---------------------------------------------------------------------------
class Exportador:
    def __init__(self, salida):
        self.salida = salida
        self.autores, self.obras, self.tradiciones = {}, {}, {}
        for carpeta, dic in (("Autores", self.autores), ("Obras", self.obras),
                             ("Tradiciones", self.tradiciones)):
            for ruta in sorted((BIB / carpeta).glob("*.md")):
                dic[ruta.stem] = leer_nota(ruta)
        self.carpeta_de = {}
        for nombre in self.autores:
            self.carpeta_de[nombre] = "Autores"
        for nombre in self.tradiciones:
            self.carpeta_de[nombre] = "Tradiciones"
        for nombre in self.obras:
            self.carpeta_de[nombre] = "Obras"

        self.obras_de_autor = defaultdict(list)
        self.obras_de_trad = defaultdict(list)
        self.autores_de_trad = defaultdict(set)
        for nombre, (meta, _) in self.obras.items():
            for a in lista(meta.get("autor")):
                self.obras_de_autor[destino(a)[0]].append(nombre)
            for t in lista(meta.get("tradiciones")) + lista(meta.get("puente_con")):
                self.obras_de_trad[destino(t)[0]].append(nombre)
        for nombre, (meta, _) in self.autores.items():
            for t in lista(meta.get("tradiciones")) + lista(meta.get("puente_con")):
                self.autores_de_trad[destino(t)[0]].add(nombre)

    # -- enlaces -------------------------------------------------------------
    def link(self, enlace, desde):
        objetivo, texto = destino(enlace)
        carpeta = self.carpeta_de.get(objetivo)
        if not carpeta:
            return texto
        ruta = f"{carpeta}/{objetivo}.md" if desde == "raiz" else f"../{carpeta}/{objetivo}.md"
        return f"[{texto}]({quote(ruta)})"

    def links(self, valores, desde):
        return ", ".join(self.link(v, desde) for v in lista(valores)) or "—"

    def link_obra(self, nombre, desde):
        meta = self.obras[nombre][0]
        titulo = meta.get("titulo") or nombre
        return self.link(f"[[{nombre}|{titulo}]]", desde)

    # -- formatos ------------------------------------------------------------
    @staticmethod
    def anio(v):
        if v is None:
            return "?"
        return f"{-v} a. C." if v < 0 else str(v)

    def vida(self, meta):
        if meta.get("nacimiento") is None and meta.get("muerte") is None:
            return "—"
        return f"{self.anio(meta.get('nacimiento'))} – {self.anio(meta.get('muerte'))}"

    @staticmethod
    def frontmatter(meta, campos, tipo):
        out = ["---", f"tipo: {tipo}"]
        for c in campos:
            v = meta.get(c)
            if v in (None, [], ""):
                continue
            out.append(f"{c}: {json.dumps(v, ensure_ascii=False)}")
        out.append("---")
        return "\n".join(out)

    # -- páginas ---------------------------------------------------------------
    def pagina_autor(self, nombre, meta, cuerpo):
        p = [self.frontmatter(meta, CAMPOS_AUTOR, "autor"), "", f"# {nombre}", ""]
        p.append(f"**{self.vida(meta)}** · {meta.get('origen') or 'origen sin datos'}")
        if not meta.get("datos_verificados"):
            p.append("")
            p.append("*Fechas y origen en revisión.*")
        p += ["", "| | |", "|---|---|",
              f"| Ala | {ALAS.get(meta.get('ala'), '—')} |",
              f"| Tradiciones | {self.links(meta.get('tradiciones'), 'sub')} |",
              f"| Cruces con la otra ala | {self.links(meta.get('puente_con'), 'sub')} |",
              f"| Etiquetas | {', '.join(lista(meta.get('etiquetas'))) or '—'} |", ""]
        for titulo, texto in secciones(cuerpo, SECCIONES_AUTOR).items():
            p += [f"## {titulo}", "", texto, ""]
        obras = sorted(self.obras_de_autor.get(nombre, []))
        p += ["## Obras en la biblioteca", ""]
        p += [f"- {self.link_obra(o, 'sub')}" for o in obras] or ["- —"]
        return "\n".join(p) + "\n"

    def pagina_obra(self, nombre, meta, cuerpo):
        titulo = meta.get("titulo") or nombre
        autores = self.links(meta.get("autor"), "sub") if meta.get("autor") else "Anónimo o tradicional"
        p = [self.frontmatter(meta, CAMPOS_OBRA, "obra"), "", f"# {titulo}", "",
             f"**{autores}**", "", "| | |", "|---|---|",
             f"| Ala | {ALAS.get(meta.get('ala'), '—')} |",
             f"| Tradiciones | {self.links(meta.get('tradiciones'), 'sub')} |",
             f"| Cruces con la otra ala | {self.links(meta.get('puente_con'), 'sub')} |",
             f"| Etiquetas | {', '.join(lista(meta.get('etiquetas'))) or '—'} |",
             f"| Estado | {LECTURA.get(meta.get('lectura'), meta.get('lectura') or '—')} |", ""]
        for t, texto in secciones(cuerpo, SECCIONES_OBRA).items():
            p += [f"## {t}", "", texto, ""]
        return "\n".join(p) + "\n"

    def pagina_tradicion(self, nombre, meta, cuerpo):
        p = ["---", "tipo: tradicion", f"ala: {json.dumps(meta.get('ala'))}", "---", "",
             f"# {nombre}", "", f"Ala {ALAS.get(meta.get('ala'), '—')} · {meta.get('area') or ''}", ""]
        for titulo, texto in secciones(cuerpo, SECCIONES_TRADICION).items():
            p += [f"## {titulo}", "", texto, ""]
        autores = sorted(self.autores_de_trad.get(nombre, []),
                         key=lambda a: (self.autores[a][0].get("nacimiento") is None,
                                        self.autores[a][0].get("nacimiento") or 0))
        p += ["## Autores", "", "| Autor | Vida | Origen |", "|---|---|---|"]
        for a in autores:
            m = self.autores[a][0]
            p.append(f"| {self.link(f'[[{a}]]', 'sub')} | {self.vida(m)} | {m.get('origen') or '—'} |")
        p += ["", "## Obras", ""]
        p += [f"- {self.link_obra(o, 'sub')}" for o in sorted(set(self.obras_de_trad.get(nombre, [])))] or ["- —"]
        return "\n".join(p) + "\n"

    def catalogo(self):
        p = ["# Catálogo de la Biblioteca", "",
             f"{len(self.obras)} obras · {len(self.autores)} autores · {len(self.tradiciones)} tradiciones", "",
             "Las fechas y el origen de los autores están en revisión.", ""]
        por_ala = defaultdict(lambda: defaultdict(list))
        for nombre, (meta, _) in self.tradiciones.items():
            por_ala[meta.get("ala")][meta.get("area") or "Otras"].append(nombre)
        for ala in ("exoterica", "esoterica", "puente"):
            if ala not in por_ala:
                continue
            p += [f"## Ala {ALAS[ala]}", ""]
            for area in sorted(por_ala[ala]):
                p += [f"### {area}", "", "| Tradición | Autores | Obras |", "|---|---|---|"]
                for t in sorted(por_ala[ala][area]):
                    link = f"[{t}]({quote('Tradiciones/' + t + '.md')})"
                    p.append(f"| {link} | {len(self.autores_de_trad.get(t, []))} | "
                             f"{len(set(self.obras_de_trad.get(t, [])))} |")
                p.append("")
        p += ["## Autores", "", "| Autor | Vida | Origen | Ala | Obras |", "|---|---|---|---|---|"]
        for a in sorted(self.autores, key=str.casefold):
            m = self.autores[a][0]
            p.append(f"| [{a}]({quote('Autores/' + a + '.md')}) | {self.vida(m)} | "
                     f"{m.get('origen') or '—'} | {ALAS.get(m.get('ala'), '—')} | "
                     f"{len(self.obras_de_autor.get(a, []))} |")
        return "\n".join(p) + "\n"

    def readme(self):
        alas = defaultdict(int)
        for meta, _ in self.obras.values():
            alas[meta.get("ala")] += 1
        return f"""# Proyecto Alejandría

Sistema de curaduría cultural construido sobre **Obsidian** y **Claude**, que convierte una
biblioteca personal de filosofía, literatura y tradiciones espirituales en la fuente de un
proyecto de divulgación y educación.

## La biblioteca

| | |
|---|---|
| Obras | {len(self.obras)} |
| Autores | {len(self.autores)} |
| Tradiciones | {len(self.tradiciones)} |
| Ala exotérica | {alas['exoterica']} obras |
| Ala esotérica | {alas['esoterica']} obras |
| Ala puente (textos sagrados y mitología) | {alas['puente']} obras |

👉 **[Ver el catálogo completo](Biblioteca/{quote('Catálogo.md')})**

La biblioteca tiene dos alas: la **exotérica** (filosofía, literatura, historia, ciencias) y la
**esotérica** (ocultismo, mística, tradiciones espirituales). Los cruces entre ambas se marcan
explícitamente: son la veta más distintiva del proyecto.

## Cómo funciona

```
Biblioteca (PDF)  →  Vault de Obsidian  →  Contenido (Instagram, web, newsletter)  →  Cursos
                     fichas + metadatos      redactado desde las fichas
```

- **La clasificación vive en metadatos, no en carpetas.** Cada obra y cada autor lleva
  `ala`, `tradiciones`, `puente_con` y `etiquetas` en su frontmatter. Las vistas se arman
  con el plugin Bases de Obsidian, así una obra puede pertenecer a varias tradiciones a la vez.
- **Herencia.** Las obras heredan la clasificación de su autor salvo que tengan clasificación propia.
- **Destilar una vez.** Cada obra se lee una sola vez para escribir su ficha de lectura;
  después todo el trabajo (contenido, cursos) parte de la ficha. Es lo que hace sostenible
  trabajar con una IA sobre cientos de libros.
- **Humano + IA.** El curador decide y publica; Claude destila, conecta y redacta siguiendo
  las reglas de [`Sistema/CLAUDE.md`](Sistema/CLAUDE.md).

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| [`Biblioteca/`](Biblioteca/) | Catálogo público: autores, obras y tradiciones |
| [`Sistema/Plantillas/`](Sistema/Plantillas/) | Plantillas de notas (obra, autor, carrusel, curso…) |
| [`Sistema/Bases/`](Sistema/Bases/) | Vistas dinámicas de Obsidian Bases |
| [`Sistema/Scripts/`](Sistema/Scripts/) | `poblar.py` (genera las fichas desde la biblioteca) y `exportar.py` (genera este repositorio) |
| [`Sistema/Diseño del vault.md`]({quote('Sistema/Diseño del vault.md')}) | Documento de diseño |

## Qué no está acá

Este repositorio es la parte pública del vault. No incluye los libros, las rutas de archivo
ni el contenido destilado de las obras, que es la materia prima de los cursos.

---

*Generado automáticamente con `Sistema/Scripts/exportar.py`.*
"""

    # -- ejecución -------------------------------------------------------------
    def archivos(self):
        """Devuelve {ruta relativa: contenido (str) o Path de origen}."""
        f = {"README.md": self.readme(), "Biblioteca/Catálogo.md": self.catalogo(),
             MARCA: "Carpeta generada por exportar.py\n"}
        for n, (m, c) in self.autores.items():
            f[f"Biblioteca/Autores/{n}.md"] = self.pagina_autor(n, m, c)
        for n, (m, c) in self.obras.items():
            f[f"Biblioteca/Obras/{n}.md"] = self.pagina_obra(n, m, c)
        for n, (m, c) in self.tradiciones.items():
            f[f"Biblioteca/Tradiciones/{n}.md"] = self.pagina_tradicion(n, m, c)
        for item in SISTEMA_PUBLICO:
            origen = SISTEMA / item
            rutas = [origen] if origen.is_file() else sorted(p for p in origen.rglob("*") if p.is_file())
            for r in rutas:
                rel = "Sistema/" + r.relative_to(SISTEMA).as_posix()
                f[rel] = limpiar_rutas(r.read_text(encoding="utf-8"))
        return f


def limpiar_rutas(texto):
    texto = re.sub(r"C:\\Users\\[^\\`\s]+\\Documents\\Biblioteca", "<ruta de la Biblioteca>", texto)
    texto = re.sub(r"C:\\Users\\[^\\`\s]+\\Documents\\Proyecto Alejandria", "<carpeta del vault>", texto)
    return texto


FILTROS = [(r"[A-Za-z]:\\(?!ruta)", "ruta de Windows"), (r"file:///", "enlace a archivo local"),
           (r"\.(pdf|epub|docx?|odt)\b", "nombre de archivo")]


def revisar(archivos):
    """Busca rutas o nombres de archivo que se hayan colado en el catálogo."""
    problemas = []
    for rel, contenido in archivos.items():
        if not rel.startswith("Biblioteca/") and rel != "README.md":
            continue
        for patron, motivo in FILTROS:
            for m in re.finditer(patron, contenido, re.I):
                problemas.append(f"{rel}: {motivo} ({m.group(0)})")
    return problemas


def main():
    simular = "--simular" in sys.argv
    cfg = json.loads((SCRIPTS / "config.local.json").read_text(encoding="utf-8"))
    salida = Path(cfg["salida_publica"])
    exp = Exportador(salida)
    archivos = exp.archivos()
    problemas = revisar(archivos)
    print(f"Autores {len(exp.autores)} · Obras {len(exp.obras)} · Tradiciones {len(exp.tradiciones)} "
          f"· Archivos {len(archivos)}")
    if problemas:
        print("ATENCIÓN, posibles datos privados:")
        print("\n".join(problemas[:50]))
        sys.exit(1)
    if simular:
        print(f"(simulación) se escribiría en {salida}")
        return
    if salida.exists() and any(salida.iterdir()) and not (salida / MARCA).exists():
        sys.exit(f"{salida} no está vacía y no fue generada por este script. No toco nada.")
    for sub in ("Biblioteca", "Sistema"):
        if (salida / sub).exists():
            shutil.rmtree(salida / sub)
    for rel, contenido in archivos.items():
        destino_archivo = salida / rel
        destino_archivo.parent.mkdir(parents=True, exist_ok=True)
        destino_archivo.write_text(contenido, encoding="utf-8", newline="\n")
    gi = salida / ".gitignore"
    if not gi.exists():
        gi.write_text("config.local.json\n.obsidian/\n", encoding="utf-8")
    print(f"Listo: {salida}")


if __name__ == "__main__":
    main()
