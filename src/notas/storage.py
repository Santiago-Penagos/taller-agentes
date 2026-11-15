"""Persistencia en JSON utf-8 de los pares nota-peso.

No imprime ni pide datos: solo lee y escribe archivos.
"""

import json
from collections.abc import Sequence
from pathlib import Path

from . import VERSION_ESQUEMA, ParNota
from .calculos import validar


def _es_numero(valor: object) -> bool:
    """Indica si el valor es un numero JSON (bool no cuenta)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _leer_esquema(datos: object, ruta: str | Path) -> list[ParNota]:
    """Convierte el contenido decodificado en pares o lanza ``ValueError``."""
    if not isinstance(datos, dict):
        raise ValueError(
            f"el archivo {ruta} debe contener un objeto con 'version' y 'notas'"
        )

    version = datos.get("version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("la clave 'version' debe ser un entero")
    if version != VERSION_ESQUEMA:
        raise ValueError(
            f"la version del esquema debe ser {VERSION_ESQUEMA} (es {version})"
        )

    lista = datos.get("notas")
    if not isinstance(lista, list):
        raise ValueError("la clave 'notas' debe ser una lista")

    pares: list[ParNota] = []
    for indice, elemento in enumerate(lista, start=1):
        if not isinstance(elemento, dict):
            raise ValueError(f"la nota {indice} debe ser un objeto")
        if "nota" not in elemento or "peso" not in elemento:
            raise ValueError(
                f"la nota {indice} debe tener las claves 'nota' y 'peso'"
            )
        nota = elemento["nota"]
        peso = elemento["peso"]
        if not _es_numero(nota) or not _es_numero(peso):
            raise ValueError(
                f"la nota {indice} debe tener valores numericos en 'nota' y 'peso'"
            )
        pares.append((float(nota), float(peso)))
    return pares


def guardar(ruta: str | Path, notas: Sequence[ParNota]) -> None:
    """Guarda los pares en ``ruta`` como JSON utf-8.

    Valida antes de escribir y propaga ``ValueError`` si la validacion falla.
    Propaga ``OSError`` si el sistema no puede escribir el archivo.
    """
    pares = list(notas)
    validar(pares)

    datos = {
        "version": VERSION_ESQUEMA,
        "notas": [
            {"nota": float(nota), "peso": float(peso)}
            for nota, peso in pares
        ],
    }
    with Path(ruta).open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")


def cargar(ruta: str | Path) -> list[ParNota]:
    """Carga y devuelve los pares guardados en ``ruta``.

    Lanza ``FileNotFoundError`` si la ruta no existe (R6) y ``ValueError`` si
    el JSON no se puede decodificar o no respeta el esquema (R5).
    """
    with Path(ruta).open("r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"el archivo {ruta} no contiene JSON valido"
            ) from exc
    return _leer_esquema(datos, ruta)
