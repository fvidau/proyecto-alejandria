---
tipo: curso
estado: idea
recorrido: 
ala: 
tradiciones: []
---

# {{title}}

## Promesa
<!-- Qué transformación ofrece, en una frase -->

## Para quién es


## Módulos

```base
filters:
  and:
    - tipo == "modulo"
    - file.hasLink(this.file)
views:
  - type: table
    name: Módulos
    order:
      - orden
      - file.name
      - estado
    sort:
      - property: orden
        direction: ASC
```
