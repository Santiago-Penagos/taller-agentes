"""Paquete de la calculadora de notas ponderadas.

Define el tipo compartido y las constantes del formato que usan las capas.
"""

# Tipo compartido: (nota, peso). Nunca se usan listas paralelas.
ParNota = tuple[float, float]

NOTA_MIN = 0.0
NOTA_MAX = 5.0
PESO_TOTAL = 100.0
TOLERANCIA_PESOS = 0.01
DECIMALES = 2
VERSION_ESQUEMA = 1

__all__ = [
    "ParNota",
    "NOTA_MIN",
    "NOTA_MAX",
    "PESO_TOTAL",
    "TOLERANCIA_PESOS",
    "DECIMALES",
    "VERSION_ESQUEMA",
]
