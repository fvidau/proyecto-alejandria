# Proyecto Alejandría

Sistema de curaduría cultural construido sobre **Obsidian** y **Claude**, que convierte una
biblioteca personal de filosofía, literatura y tradiciones espirituales en la fuente de un
proyecto de divulgación y educación.

## La biblioteca

| | |
|---|---|
| Obras | 848 |
| Autores | 381 |
| Tradiciones | 55 |
| Ala exotérica | 628 obras |
| Ala esotérica | 203 obras |
| Ala puente (textos sagrados y mitología) | 17 obras |

👉 **[Ver el catálogo completo](Biblioteca/Cat%C3%A1logo.md)**

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
| [`Sistema/Diseño del vault.md`](Sistema/Dise%C3%B1o%20del%20vault.md) | Documento de diseño |

## Qué no está acá

Este repositorio es la parte pública del vault. No incluye los libros, las rutas de archivo
ni el contenido destilado de las obras, que es la materia prima de los cursos.

---

*Generado automáticamente con `Sistema/Scripts/exportar.py`.*
