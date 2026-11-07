---
tipo: autor
nombre: "{{title}}"
alias: []
ala: 
tradiciones: []
puente_con: []
etiquetas: []
nacimiento: 
muerte: 
origen: 
datos_verificados: false
estado: semilla
---

# {{title}}

## Quién fue
<!-- 3 a 5 líneas: época, lugar, vida, obra principal -->

## Por qué importa para Alejandría
<!-- Qué aporta al proyecto. ¿Qué pregunta responde? ¿Con qué otra ala dialoga? -->

## Obras en la biblioteca

```base
filters:
  and:
    - tipo == "obra"
    - file.hasLink(this.file)
views:
  - type: table
    name: Obras
    order:
      - file.name
      - lectura
      - prioridad
```

## Conexiones
<!-- Maestros, discípulos, influencias, oponentes. Enlazar con [[ ]] -->
