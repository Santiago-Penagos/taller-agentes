# Idea: calculadora de notas ponderadas

Programa de consola en Python que calcula el promedio ponderado de una materia.

Reglas:
- Cada nota va de 0 a 5.
- Cada nota tiene un peso en porcentaje; los pesos deben sumar 100.
- Una lista vacía de notas es un error.
- Se pueden guardar y cargar las notas desde un archivo JSON.
- La suma de los pesos se acepta con una tolerancia de 0.01 (por ejemplo, 33.33 + 33.33 + 33.34 es válido).
- El promedio se redondea a 2 decimales.