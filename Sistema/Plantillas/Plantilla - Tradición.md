---
tipo: tradicion
ala: 
padre: 
---

# {{title}}

## Qué es
<!-- Texto curatorial breve: origen, idea central, por qué importa hoy -->

## Por dónde empezar
<!-- 2 o 3 obras de entrada, en orden -->
1. 

## Autores

```base
filters:
  and:
    - tipo == "autor"
    - file.hasLink(this.file)
views:
  - type: table
    name: Autores
    order:
      - file.name
      - nacimiento
      - muerte
      - origen
    sort:
      - property: nacimiento
        direction: ASC
```

## Obras

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
      - autor
      - lectura
```
