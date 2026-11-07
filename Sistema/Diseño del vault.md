# Diseño — Vault "Proyecto Alejandría"

*Versión 1 · 06/11/2026 · Autores: el creador del proyecto y Claude*

---

## 1. Intención

Proyecto Alejandría es un proyecto cultural, educativo y de sabiduría que hoy existe como:

- una cuenta de Instagram (`@la.biblioteca.de.alejandria`, ~1.300 seguidores, estética de pintura clásica + texto),
- una biblioteca personal de ~865 obras (PDF casi todo) en `<ruta de la Biblioteca>`, clasificada en carpetas por categoría,
- un índice previo (`Biblioteca\Indice\ÍNDICE_BIBLIOTECA.md` y `libros.csv`).

El vault de Obsidian es **la cocina del proyecto**: el lugar donde vive la curaduría y desde donde se producen todos los productos. No lo ven los alumnos ni el público; ven lo que sale de él.

El equipo somos dos: **el creador** (curador, decide, revisa y publica) y **Claude** (destila lecturas, propone conexiones, redacta contenidos). El vault está diseñado para que Claude trabaje sobre él de forma eficiente: leer fichas ya destiladas en lugar de PDF completos, filtrar por metadatos en lugar de abrir archivos, y arrancar cada sesión sabiendo las reglas del proyecto.

### Para qué sirve, en orden de prioridad

1. **Alimentar un embudo de contenido**: Instagram (atraer) → sitio web y newsletter (profundizar) → servicio educativo online (convertir).
2. **Ser la base del servicio educativo**: los cursos se arman como recorridos curados por la biblioteca.
3. **Ordenar y comprender la biblioteca**, con dos alas:
   - **Exotérica**: autores clásicos de literatura, filosofía, historia y ciencias.
   - **Esotérica**: autores ocultistas, místicos y espirituales.
   - **Puente**: obras que pertenecen a un ala pero alimentan a la otra (neoplatonismo, Jung, mitología, sufismo, literatura ocultista, textos sagrados). Es la veta de contenido más distintiva del proyecto.

## 2. Objetivos, no-objetivos y anti-objetivos

**Objetivos**

- Toda obra de la biblioteca tiene una ficha en el vault, enlazada a su autor y a su(s) tradición(es).
- Cualquier contenido publicado queda enlazado a las obras de las que salió.
- Claude puede producir un post, un artículo o una lección leyendo solo notas del vault, sin reabrir PDF ya destilados.
- El creador puede reclasificar un autor cambiando una línea, y los índices se actualizan solos.

**No-objetivos (por ahora)**

- No se construye el sitio web ni la plataforma de cursos. El vault queda listo para alimentarlos.
- No se define el formato del servicio educativo (grabado, en vivo, membresía): la estructura de Academia sirve para cualquiera.
- No se producen videos ni imágenes fotográficas: el creador no hace video ni diseño. El contenido es texto + arte de dominio público.
- No se reorganizan las carpetas físicas de la biblioteca en la primera etapa.

**Anti-objetivos (sería un fracaso aunque "funcione")**

- Un vault que es un volcado de 865 fichas vacías que nadie completa.
- Depender de muchos plugins comunitarios que se rompen o que el creador no entiende.
- Romper, mover o borrar archivos de la biblioteca original sin aprobación explícita.
- Distribuir a alumnos o al público textos completos con derechos vigentes.

## 3. Restricciones

- **Idioma**: todo en español.
- **Sistema**: Windows 11. Obsidian (versión actual, con el plugin núcleo **Bases** para vistas de tabla).
- **Biblioteca**: queda donde está (`<ruta de la Biblioteca>`). El vault la enlaza, no la copia.
- **Respaldo**: hoy la carpeta Documentos no está en OneDrive. Ver §10.
- **Derechos de autor**: el material para alumnos y público usa fichas, resúmenes propios y citas breves. Los textos completos solo si la obra es de dominio público: autor **y traductor** fallecidos hace más de 70 años (regla argentina). Un Platón traducido en 1980 no es libre aunque Platón sí. Es un indicador, no asesoramiento legal.

## 4. Decisiones tomadas

| Decisión | Quién decidió |
|---|---|
| El vault es interno; alumnos y público reciben material armado | Creador |
| Orientado a creación de contenido + servicio educativo | Creador |
| Dos alas: exotérica y esotérica | Creador |
| La clasificación actual tiene errores y se revisa | Creador |
| Filosofía Argentina agrupa autores **por origen** (son argentinos), no por tema | Creador ("sí") — *confirmar interpretación* |
| Mitología: **puente** (pertenece a la esotérica por tradición, se etiqueta puente) | Claude — el creador no estaba seguro |
| Formato educativo: a definir más adelante | Creador |
| Nombre: Proyecto Alejandría | Tomado del índice existente |
| Ubicación: `<carpeta del vault>` | Claude |
| Clasificación vive en metadatos de la ficha, no en carpetas | Claude |
| Un autor puede tener varias tradiciones | Claude |
| PDF enlazados con `file:///`, no copiados | Claude |
| Usar Bases (núcleo de Obsidian) en vez de Dataview | Claude |
| Las obras heredan la clasificación del autor, con excepción por obra (§6.1) | Claude |
| Tras la etapa 2, **el vault es la fuente de verdad**; la tabla de revisión queda como histórico | Claude |
| Textos Sagrados y Mitología: `ala: puente` (tercera sala) | Claude |
| Dominio público se evalúa por obra (autor **y** traductor); por defecto "sin verificar" | Claude |
| Fechas y origen de autores: los completa Claude en la etapa 2, marcados "sin verificar" | Claude |
| En filas de la tabla con dos opciones, se toma la primera | Claude |
| "Por origen" aplica a Filosofía, Historia y Literatura Argentina por igual (incluye a Alberdi en Filosofía Argentina con sus obras filosóficas) | Claude |

## 5. Estructura de carpetas

```
Proyecto Alejandria/
├── 00 Sistema/
│   ├── CLAUDE.md               ← instrucciones para Claude (ver §7)
│   ├── Plantillas/             ← una por tipo de nota
│   ├── Bases/                  ← vistas: obras por ala, por estado, por tradición…
│   └── Diseño del vault.md     ← este documento
├── 10 Biblioteca/
│   ├── Autores/                ← una nota por autor
│   ├── Obras/                  ← una nota por obra (incluye la ficha de lectura)
│   ├── Tradiciones/            ← una nota por tradición (índice + texto curatorial)
│   ├── Conceptos/              ← ideas que cruzan autores: Logos, Uno, Gnosis, Voluntad…
│   ├── Ala Exotérica.md        ← mapa de entrada del ala
│   ├── Ala Esotérica.md
│   └── Puentes.md              ← mapa de los cruces entre alas
├── 20 Contenido/
│   ├── Ideas/                  ← banco de ideas (una nota corta por idea)
│   ├── Piezas/                 ← carruseles, posts, artículos, newsletters
│   ├── Series/                 ← series recurrentes ("Un autor por semana"…)
│   └── Calendario.md
├── 30 Academia/
│   ├── Cursos/                 ← curso → módulos → lecciones
│   └── Recorridos/             ← itinerarios de lectura (insumo de cursos e imanes)
├── 40 Marca/
│   ├── Voz y estilo.md
│   ├── Público.md
│   ├── Embudo.md
│   └── Imanes/                 ← guías gratuitas para captar suscriptores
└── 90 Archivo/                 ← lo descartado, nunca se borra
```

Las carpetas organizan **tipos de nota**. La clasificación temática (ala, tradición, época) vive en los metadatos y se muestra con Bases.

## 6. Tipos de nota y metadatos

Todos los campos en minúsculas sin tildes para que las consultas sean simples. Los valores de texto libre sí llevan tildes.

### Autor (`10 Biblioteca/Autores/Nombre Apellido.md`)

```yaml
tipo: autor
nombre: "Jakob Böhme"
alias: ["Boehme", "Böheme"]        # variantes que aparecen en los archivos
ala: esoterica                      # exoterica | esoterica | puente
tradiciones: ["[[Mística cristiana]]", "[[Hermetismo y Alquimia]]"]
puente_con: []                      # tradiciones del OTRA ala que alimenta
etiquetas: []                       # transversales: literatura-ocultista, sufismo, estudio-academico…
nacimiento: 1575
muerte: 1624
origen: "Alemania"
datos_verificados: false            # fechas/origen cargados por Claude hasta que se revisen
estado: semilla                     # semilla | en-desarrollo | completo
```

Cuerpo: quién fue (3–5 líneas), por qué importa para el proyecto, obras (vista automática), conexiones con otros autores.

### Obra (`10 Biblioteca/Obras/Autor - Título.md`)

```yaml
tipo: obra
titulo: "La llave"
autor: "[[Jakob Böhme]]"
ala: esoterica
tradiciones: ["[[Mística cristiana]]"]
puente_con: []
etiquetas: []
clasificacion_propia: false         # true = no hereda del autor (ej. Evola político, novelas de Crowley)
archivo: "Ocultismo y Esoterismo/Gnosticismo y Mística Cristiana/Böheme - La llave.pdf"   # relativo a la Biblioteca
formato: pdf
traductor: ""
dominio_publico: sin-verificar      # si | no | sin-verificar (autor Y traductor fallecidos hace +70 años)
lectura: sin-leer                   # sin-leer | leyendo | leida | destilada
prioridad: media                    # alta | media | baja (para destilar)
duplicados: []                      # otras rutas de la misma obra
usada_en: []                        # se llena al crear piezas de contenido
```

Cuerpo = **ficha de lectura** (se completa al destilar):

1. **En una frase**
2. **Resumen** (≤ 300 palabras)
3. **Ideas clave** (5–10 viñetas, cada una enlazable a un Concepto)
4. **Citas** (textuales, con página, ≤ 40 palabras cada una)
5. **Conexiones** (con otras obras y autores, especialmente cruces de ala)
6. **Ángulos de contenido** (3–5 ideas de posts o lecciones que salen de esta obra)

### 6.1 Reglas de clasificación

- **Herencia**: cada obra copia `ala`, `tradiciones`, `puente_con` y `etiquetas` de su autor (Bases necesita los campos en la propia obra). Si `clasificacion_propia: true`, la obra tiene la suya.
- **Reclasificar un autor** = editar su ficha y pedirle a Claude "propagá la clasificación de X": se actualizan sus obras que no tienen `clasificacion_propia`.
- **Fuente de verdad**: después de la etapa 2, el vault. El script de poblado, si se vuelve a ejecutar, **solo crea notas nuevas y completa campos vacíos**; nunca pisa metadatos ni cuerpo existentes.
- **Rutas**: `archivo` es relativo a la Biblioteca. La ruta base vive en un solo lugar (`00 Sistema/CLAUDE.md` y la configuración del script), así que si la Biblioteca se mueve (por ejemplo, a OneDrive) se cambia una línea. El enlace clicable `file:///` se arma en la plantilla a partir de esa base.
- **Puente**: tercera sala (`ala: puente`) solo para Textos Sagrados y Mitología. El resto de los cruces se marcan con `puente_con` y aparecen en `Puentes.md`.

### Tradición (`10 Biblioteca/Tradiciones/…`)

```yaml
tipo: tradicion
ala: esoterica
padre: "[[Ala Esotérica]]"
```

Cuerpo: texto curatorial breve (qué es, por qué importa, por dónde empezar) + vista automática de autores y obras.

### Concepto, Idea, Pieza, Curso/Módulo/Lección

- **Concepto**: `tipo: concepto`, `alas: [exoterica, esoterica]`, definición propia, autores que lo trabajan.
- **Idea**: `tipo: idea`, `fuentes: [[obra]]`, `formato_sugerido`, `etapa: atraer | profundizar | convertir`.
- **Pieza**: `tipo: pieza`, `formato: carrusel | post | articulo | newsletter | iman`, `estado: borrador | revision | lista | publicada`, `canal`, `fecha`, `serie`, `fuentes: [[obras]]`, `etapa`.
- **Curso / Módulo / Lección**: `tipo` correspondiente, `curso`, `orden`, `fuentes`, `estado`. Sin campos de formato de entrega (todavía no definido).

## 7. Cómo trabaja Claude en el vault (ahorro de tokens)

`00 Sistema/CLAUDE.md` contiene, en este orden:

1. Qué es el proyecto y el embudo (resumen de §1).
2. **Reglas de lectura**: buscar primero por metadatos y Bases; leer la ficha de la obra antes que el PDF; abrir un PDF solo para destilarlo o verificar una cita.
3. **Cómo destilar una obra**: completar la ficha de §6 en una sola pasada y marcar `lectura: destilada`.
4. **Voz y estilo** (enlace a `40 Marca/Voz y estilo.md`).
5. **Cómo producir cada formato** (enlace a plantillas).
6. **Reglas de derechos** (§3).
7. **Nunca** mover, renombrar ni borrar archivos de la Biblioteca sin aprobación.

## 8. Flujos de trabajo

**Destilar** (convierte un PDF en conocimiento reutilizable):
el creador elige una obra (o Claude propone según `prioridad`) → Claude lee el PDF una vez → completa la ficha → crea o enlaza Conceptos → propone ángulos de contenido como notas en `Ideas/`.

**Producir contenido**:
el creador elige una idea o una serie → Claude redacta la pieza desde las fichas, con la plantilla del formato → el creador revisa → se marca `publicada` y se registra en `usada_en` de cada obra fuente.

**Armar un curso** (más adelante):
un Recorrido de lectura → se convierte en módulos → cada lección enlaza obras y conceptos destilados.

## 9. Plan de construcción por etapas

| Etapa | Qué se hace | Resultado |
|---|---|---|
| 1. Esqueleto | Carpetas, plantillas, `CLAUDE.md`, Bases, notas de Marca vacías con preguntas guía | Vault abrible y navegable |
| 2. Poblado automático | Un script lee la Biblioteca, aplica la tabla de reclasificación aprobada y la normalización de nombres, y genera notas de Autor, Obra y Tradición con metadatos (cuerpo vacío). Claude completa fechas y origen de los autores desde su conocimiento (`datos_verificados: false`); el creador revisa por muestreo | ~865 obras, ~400 autores, ~50 tradiciones |
| 3. Limpieza física (opcional) | Borrar duplicados y archivos ajenos, previa aprobación archivo por archivo; regenerar enlaces | Biblioteca limpia |
| 4. Piloto de destilación | 3–5 obras elegidas por el creador, idealmente "puente" | Validar formato de la ficha |
| 5. Piloto de contenido | Definir voz, 1 serie, plantilla de carrusel, 1 semana de calendario | Primeras piezas desde el vault |

Al terminar cada etapa, el creador revisa antes de seguir.

## 10. Pendientes del creador (no bloquean la etapa 1)

- Aprobar o corregir la tabla de reclasificación (`revision-clasificacion.md`). **Por defecto se aplican todas las propuestas** salvo las que el creador marque; cualquier cambio posterior es editar una línea.
- Decidir qué hacer con los duplicados y con archivos ajenos al proyecto (ej. *Automate the Boring Stuff with Python*).
- Respaldo: mover Biblioteca y vault a OneDrive o configurar otro respaldo.
- Formato del servicio educativo.
- Revisar si Google Drive tiene material que no esté en la Biblioteca local (se asume que no).

## 11. Lo que queda a criterio del constructor

- Nombres exactos de las Bases y sus columnas.
- Redacción de las plantillas y de las preguntas guía de Marca.
- Cómo se calcula el año de autores sin fecha conocida (dejar vacío y marcar `estado: semilla`).
- Detalles del script de poblado (lenguaje, idempotencia), siempre que sea **re-ejecutable sin pisar notas ya completadas**.
