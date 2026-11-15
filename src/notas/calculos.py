"""Logica pura: validacion de pares nota-peso y calculo del promedio.

No lee entrada, no escribe en pantalla y no accede al disco.
"""

import math
from collections.abc import Sequence
from decimal import ROUND_HALF_UP, Decimal

from . import (
    DECIMALES,
    NOTA_MAX,
    NOTA_MIN,
    PESO_TOTAL,
    TOLERANCIA_PESOS,
    ParNota,
)

# Cuantizador con la cantidad de decimales del contrato (0.01 para 2 decimales).
_CUANTIZADOR = Decimal(1).scaleb(-DECIMALES)
# Cota inferior de cada peso; la superior es PESO_TOTAL.
_PESO_MIN = 0.0


def _es_numero(valor: object) -> bool:
    """Indica si el valor es un numero real finito (bool no cuenta)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return False
    return math.isfinite(valor)


def _suma_pesos_exacta(notas: Sequence[ParNota]) -> Decimal:
    """Suma los pesos con ``Decimal`` para respetar el limite de tolerancia."""
    total = Decimal(0)
    for _, peso in notas:
        total += Decimal(str(peso))
    return total


def validar(notas: Sequence[ParNota]) -> None:
    """Valida los pares nota-peso.

    Recibe una secuencia de tuplas ``(nota, peso)`` y no devuelve nada.
    Lanza ``ValueError`` si la lista esta vacia (R3), si una nota sale de
    [0, 5] (R1), si un peso sale de [0, 100] o si los pesos no suman
    100 +- 0.01 (R2).
    """
    pares = list(notas)
    if not pares:
        raise ValueError("la lista de notas no puede estar vacia")

    for indice, par in enumerate(pares, start=1):
        try:
            nota, peso = par
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"el par {indice} debe contener una nota y un peso"
            ) from exc
        if not _es_numero(nota):
            raise ValueError(f"la nota del par {indice} debe ser un numero")
        if not _es_numero(peso):
            raise ValueError(f"el peso del par {indice} debe ser un numero")
        if nota < NOTA_MIN or nota > NOTA_MAX:
            raise ValueError(
                f"la nota del par {indice} debe estar entre "
                f"{NOTA_MIN} y {NOTA_MAX}"
            )
        if peso < _PESO_MIN or peso > PESO_TOTAL:
            raise ValueError(
                f"el peso del par {indice} debe estar entre "
                f"{_PESO_MIN} y {PESO_TOTAL}"
            )

    total = _suma_pesos_exacta(pares)
    if abs(total - Decimal(str(PESO_TOTAL))) > Decimal(str(TOLERANCIA_PESOS)):
        raise ValueError(
            f"los pesos deben sumar {PESO_TOTAL} (suman {total})"
        )


def suma_pesos(notas: Sequence[ParNota]) -> float:
    """Devuelve la suma de los pesos. No valida los pares."""
    total = 0.0
    for _, peso in notas:
        total += peso
    return total


def promedio(notas: Sequence[ParNota]) -> float:
    """Devuelve el promedio ponderado redondeado a 2 decimales.

    Valida primero los pares y propaga ``ValueError`` (R1, R2, R3).
    Redondea con ``Decimal`` y ``ROUND_HALF_UP`` (mitad hacia arriba, R4).
    """
    pares = list(notas)
    validar(pares)

    suma = Decimal(0)
    for nota, peso in pares:
        suma += Decimal(str(nota)) * Decimal(str(peso))

    valor = suma / Decimal(str(PESO_TOTAL))
    redondeado = valor.quantize(_CUANTIZADOR, rounding=ROUND_HALF_UP)
    return float(redondeado)
