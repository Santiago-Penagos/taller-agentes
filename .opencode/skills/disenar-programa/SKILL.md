---
name: disenar-programa
description: Convierte docs/idea.md en un contrato técnico en capas con firmas, esquema JSON y reglas de aceptación numeradas. Úsala antes de escribir código o pruebas.
---

# Diseñar programa

## Cuándo usarla

Antes de escribir cualquier archivo en `src/` o `tests/`, y siempre que `docs/idea.md` cambie. Su salida es `docs/diseno.md`, el contrato que leen los demás roles.

## Entradas y salida

- Entrada: `docs/idea.md` y, si existe, la versión anterior de `docs/diseno.md`.
- Salida: `docs/diseno.md` con todas las secciones de la plantilla.

## Pasos

1. Lee `docs/idea.md` completo. Anota cada regla explícita y cada caso límite que se deduzca de ella.
2. Descompón el programa en tres capas, una responsabilidad por capa: lógica pura (validar y calcular, sin entrada, salida ni disco), persistencia (leer y escribir el formato de datos) y presentación (pedir datos, mostrar resultados y manejar errores).
3. Fija el árbol de archivos a partir de esas capas. Los nombres de módulos y funciones deben ser estables, porque el Tester los usa como interfaz.
4. Define la interfaz pública de cada módulo: nombre, firma, tipos de retorno y error esperado. El texto de los mensajes queda libre; el tipo de error no.
5. Define el esquema JSON con un número de versión y una lista de pares nota-peso. Evita listas paralelas que puedan desalinearse.
6. Numera las reglas de aceptación R1..R6 usando el catálogo obligatorio. Cada regla debe poder verificarse con una prueba y tener un resultado esperado inequívoco.
7. Escribe `docs/diseno.md` con la plantilla.
8. Revisa el checklist y corrige el contrato antes de terminar.

## Catálogo obligatorio de reglas

| Regla | Enunciado |
|---|---|
| R1 | Cada nota está en el rango [0, 5]; fuera de rango es error de validación. |
| R2 | Los pesos suman 100 con tolerancia 0.01 y hay un peso por cada nota; si no, error de validación. |
| R3 | Una lista vacía de notas es error de validación. |
| R4 | Promedio = suma(nota x peso) / 100, redondeado a 2 decimales con la mitad hacia arriba. |
| R5 | Guardar y cargar en JSON utf-8 conserva los valores y la correspondencia nota-peso. |
| R6 | Cargar un archivo inexistente es un error controlado. |

Precisiones que el contrato debe dejar explícitas: el error de validación es `ValueError`; `storage.cargar` lanza `FileNotFoundError` si el archivo no existe y `ValueError` si el contenido no respeta el esquema; el redondeo se implementa con `Decimal` y `ROUND_HALF_UP`.

## Checklist de pensamiento computacional

- [ ] Descomposición: cada módulo tiene una sola responsabilidad y no hay dependencias circulares.
- [ ] Reconocimiento de patrones: el flujo validar -> calcular -> persistir/presentar aparece explícito.
- [ ] Abstracción: la interfaz pública oculta los detalles y no filtra tipos ni estructuras internas.
- [ ] Algoritmo: la fórmula y el redondeo están escritos paso a paso, sin ambigüedad.
- [ ] Evaluación: cada regla R1..R6 tiene un caso verificable y un resultado esperado.

## Plantilla de docs/diseno.md

```markdown
# Diseño: <nombre del programa>

## 1. Objetivo
<una o dos frases, tomadas de docs/idea.md>

## 2. Capas y archivos
| Capa | Archivo | Responsabilidad |
|---|---|---|

## 3. Interfaz pública
| Módulo | Función | Firma | Retorno | Errores |
|---|---|---|---|---|

## 4. Esquema JSON
<ejemplo con version y lista de pares nota-peso>

## 5. Reglas de aceptación
| Regla | Enunciado | Verificación esperada |
|---|---|---|
| R1 | ... | ... |

## 6. Fuera de alcance
<lo que no se implementa>
```

## Formato de salida

Al terminar, informa: archivos escritos, módulos y funciones definidos, reglas cubiertas y supuestos asumidos.
