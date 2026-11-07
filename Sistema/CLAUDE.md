# Instrucciones para Claude — Proyecto Alejandría

Este vault es la **cocina** de Proyecto Alejandría: un proyecto cultural, educativo y de sabiduría. Acá vive la curaduría; afuera salen los productos (Instagram, sitio web, newsletter, cursos). El equipo somos dos: el creador (curador, decide y publica) y Claude (destila, conecta, redacta). Diseño completo: [[Diseño del vault]].

## 1. El embudo

1. **Atraer** — Instagram `@la.biblioteca.de.alejandria`: carruseles de texto sobre pintura de dominio público, citas comentadas, series.
2. **Profundizar** — sitio web y newsletter: artículos largos, imanes de suscripción (guías gratuitas).
3. **Convertir** — servicio educativo online: cursos armados como recorridos curados por la biblioteca. Formato todavía no definido.

## 2. Las alas

- **Exotérica** (`ala: exoterica`): filosofía, literatura, historia, ciencias.
- **Esotérica** (`ala: esoterica`): ocultismo, mística, tradiciones espirituales.
- **Puente** (`ala: puente`): solo Textos Sagrados y Mitología. Los demás cruces se marcan con `puente_con` y son la veta de contenido más distintiva del proyecto.

## 3. Biblioteca física

- **Ruta base:** `<ruta de la Biblioteca>`
- El campo `archivo` de cada obra es **relativo** a esa ruta. Si la Biblioteca se mueve, se cambia solo esta línea.
- **Nunca** mover, renombrar ni borrar archivos de la Biblioteca sin aprobación explícita del creador, archivo por archivo.

## 4. Reglas de lectura (ahorro de tokens)

1. Buscar primero por **metadatos** (frontmatter) y por las vistas de `00 Sistema/Bases/`. No abrir notas a ciegas.
2. Para hablar de una obra, leer su **ficha** (`10 Biblioteca/Obras/`). Si `lectura: destilada`, la ficha alcanza.
3. Abrir un PDF **solo** para destilarlo o para verificar una cita textual.
4. Leer las notas de `40 Marca/` antes de redactar cualquier pieza.

## 5. Destilar una obra

Cuando el creador pida destilar una obra:

1. Leer el PDF una sola vez (si está escaneado sin texto, avisar antes de seguir).
2. Completar la ficha con la estructura de [[Plantilla - Obra]]: En una frase · Resumen (≤ 300 palabras) · Ideas clave · Citas (textuales, con página, ≤ 40 palabras) · Conexiones · Ángulos de contenido.
3. Crear o enlazar notas en `10 Biblioteca/Conceptos/` para las ideas clave que cruzan autores.
4. Cada ángulo de contenido prometedor → una nota en `20 Contenido/Ideas/`.
5. Marcar `lectura: destilada`.

## 6. Clasificación

- Cada obra copia `ala`, `tradiciones`, `puente_con` y `etiquetas` de su autor, salvo que tenga `clasificacion_propia: true`.
- "Propagá la clasificación de X" = actualizar las obras de X que no tienen `clasificacion_propia`.
- Fechas y origen de autores cargados por Claude llevan `datos_verificados: false` hasta que el creador los revise.
- Cada obra arrancó con la clasificación de su carpeta (más las correcciones de [[Revisión de clasificación]]); el autor reúne las tradiciones de todas sus obras. Los cruces (`puente_con`) y `etiquetas` del autor se heredan a sus obras.
- **Poblado:** `00 Sistema/Scripts/poblar.py` (datos en `autores.csv` y en el propio script). Re-ejecutable: solo crea notas nuevas y completa campos vacíos. Usar `--simular` primero. Cada corrida deja un reporte en `00 Sistema/Reportes/`.

## 7. Producir contenido

1. Partir de una nota de `Ideas/` o de una serie de `Series/`.
2. Redactar desde las fichas, con la plantilla del formato (`00 Sistema/Plantillas/`).
3. Respetar [[Voz y estilo]] y [[Público]].
4. Dejar la pieza en `20 Contenido/Piezas/` con `estado: revision`. El creador revisa y publica.
5. Al publicar: `estado: publicada`, y agregar la pieza a `usada_en` de cada obra fuente.

## 8. Derechos de autor

- Al público y a los alumnos van fichas, resúmenes propios y citas breves.
- Texto completo solo si `dominio_publico: si`, que exige autor **y** traductor fallecidos hace más de 70 años. Ante la duda, `sin-verificar` y no se distribuye.
- Imágenes: obras de arte de dominio público, indicando autor, título y museo cuando se conozcan.

## 9. Convenciones

- Todo en español.
- Nombres de campos en minúsculas sin tildes; valores con tildes.
- Notas de autor: `Nombre Apellido.md`. Notas de obra: `Autor - Título.md`.
- Nada se borra: lo descartado va a `90 Archivo/`.
