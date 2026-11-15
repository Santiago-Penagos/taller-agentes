"""Presentacion por consola: datos, mensajes y codigos de salida.

Es el unico modulo que escribe en pantalla; no calcula ni toca el disco
por su cuenta.
"""

import sys
from pathlib import Path

from . import DECIMALES, ParNota
from .calculos import promedio
from .storage import cargar, guardar

CODIGO_OK = 0
CODIGO_ERROR = 1
CODIGO_USO = 2

_TEXTO_USO = """\
Uso:
  py -m src.main                        pide notas y pesos por teclado
  py -m src.main calcular [ARCHIVO]     calcula desde un archivo JSON o por teclado
  py -m src.main cargar ARCHIVO         muestra las notas de un archivo JSON
  py -m src.main guardar ARCHIVO        pide notas y las guarda en JSON
  py -m src.main ARCHIVO                calcula desde un archivo JSON
  py -m src.main ayuda                  muestra esta ayuda
"""


class _UsoIncorrecto(Exception):
    """Argumentos de linea de comandos que no corresponden a ningun uso."""


def formatear_promedio(valor: float) -> str:
    """Devuelve el promedio como texto con dos decimales, por ejemplo ``"4.25"``."""
    return f"{valor:.{DECIMALES}f}"


def _parsear_numero(texto: str) -> float:
    """Convierte un texto del usuario en float; lanza ``ValueError`` si no lo es."""
    limpio = texto.strip().replace(",", ".")
    try:
        return float(limpio)
    except ValueError as exc:
        raise ValueError(f"'{texto}' no es un numero valido") from exc


def _leer_pares() -> list[ParNota]:
    """Pide pares nota-peso por teclado hasta una linea vacia."""
    pares: list[ParNota] = []
    while True:
        try:
            texto_nota = input(
                f"Nota {len(pares) + 1} (linea vacia para terminar): "
            )
        except (EOFError, StopIteration):
            # Fin de la entrada (o un doble de prueba que agota su iterador).
            texto_nota = ""
        if not texto_nota.strip():
            break
        try:
            texto_peso = input("Peso: ")
        except (EOFError, StopIteration) as exc:
            raise ValueError("falta el peso de la ultima nota") from exc
        pares.append(
            (_parsear_numero(texto_nota), _parsear_numero(texto_peso))
        )
    return pares


def _calcular_interactivo() -> int:
    """Pide los pares, calcula el promedio y lo muestra."""
    pares = _leer_pares()
    valor = promedio(pares)
    print(f"Promedio: {formatear_promedio(valor)}")
    return CODIGO_OK


def _calcular_desde_archivo(ruta: str | Path) -> int:
    """Carga los pares de un archivo, calcula el promedio y lo muestra."""
    pares = cargar(ruta)
    valor = promedio(pares)
    print(f"Promedio: {formatear_promedio(valor)}")
    return CODIGO_OK


def _mostrar_archivo(ruta: str | Path) -> int:
    """Carga un archivo y muestra cada par nota-peso."""
    pares = cargar(ruta)
    for indice, (nota, peso) in enumerate(pares, start=1):
        print(f"{indice}. nota={nota:g} peso={peso:g}")
    return CODIGO_OK


def _guardar_interactivo(ruta: str | Path) -> int:
    """Pide los pares y los guarda en ``ruta``."""
    pares = _leer_pares()
    guardar(ruta, pares)
    print(f"Guardadas {len(pares)} notas en {ruta}")
    return CODIGO_OK


def _ejecutar(argumentos: list[str]) -> int:
    """Despacha los argumentos; usa ``_UsoIncorrecto`` para el codigo 2."""
    if not argumentos:
        return _calcular_interactivo()

    primero, resto = argumentos[0], argumentos[1:]

    if primero in ("ayuda", "-h", "--help"):
        if resto:
            raise _UsoIncorrecto("la ayuda no acepta mas argumentos")
        print(_TEXTO_USO, end="")
        return CODIGO_OK

    if primero.startswith("-"):
        raise _UsoIncorrecto(f"opcion desconocida: {primero}")

    if primero == "calcular":
        if len(resto) > 1:
            raise _UsoIncorrecto("calcular acepta como maximo una ruta")
        if resto:
            return _calcular_desde_archivo(resto[0])
        return _calcular_interactivo()

    if primero == "cargar":
        if len(resto) != 1:
            raise _UsoIncorrecto("cargar requiere exactamente una ruta")
        return _mostrar_archivo(resto[0])

    if primero == "guardar":
        if len(resto) != 1:
            raise _UsoIncorrecto("guardar requiere exactamente una ruta")
        return _guardar_interactivo(resto[0])

    if resto:
        raise _UsoIncorrecto(
            f"argumentos no reconocidos: {' '.join(resto)}"
        )
    # Una ruta suelta se interpreta como "calcular desde este archivo".
    return _calcular_desde_archivo(primero)


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la calculadora y devuelve el codigo de salida.

    ``0`` si todo va bien, ``1`` ante un error controlado (validacion,
    archivo ausente o error de disco) y ``2`` ante un uso incorrecto.
    No propaga esos errores: los convierte en mensaje y codigo.
    """
    argumentos = list(sys.argv[1:] if argv is None else argv)
    try:
        return _ejecutar(argumentos)
    except _UsoIncorrecto as exc:
        print(f"Uso incorrecto: {exc}")
        print(_TEXTO_USO, end="")
        return CODIGO_USO
    except FileNotFoundError as exc:
        nombre = exc.filename if exc.filename is not None else "indicado"
        print(f"Error: no se encontro el archivo {nombre}")
        return CODIGO_ERROR
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}")
        return CODIGO_ERROR
