---
tipo: concepto
alas: []
etiquetas: []
---

# {{title}}

## Definición
<!-- Con palabras propias, en 2 o 3 líneas -->

## Cómo lo entiende cada ala
- **Exotérica:** 
- **Esotérica:** 

## Dónde aparece

```base
filters:
  and:
    - file.hasLink(this.file)
views:
  - type: table
    name: Menciones
    order:
      - file.name
      - tipo
      - autor
```
