---
tipo: modulo
curso: 
orden: 
estado: borrador
---

# {{title}}

## Objetivo del módulo


## Lecciones

```base
filters:
  and:
    - tipo == "leccion"
    - file.hasLink(this.file)
views:
  - type: table
    name: Lecciones
    order:
      - orden
      - file.name
      - estado
    sort:
      - property: orden
        direction: ASC
```
