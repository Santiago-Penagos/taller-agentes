"""Pruebas de persistencia JSON (R5) y archivo inexistente (R6)."""

import json

import pytest

from src.notas.storage import cargar, guardar

PARES = [(4.0, 40.0), (3.5, 60.0)]


def _escribir_json(ruta, datos):
    ruta.write_text(json.dumps(datos), encoding="utf-8")


# R5: guardar y cargar en JSON utf-8 conserva valores y correspondencia.
def test_r5_guardar_y_cargar_conserva_los_pares(tmp_path):
    ruta = tmp_path / "notas.json"

    guardar(ruta, PARES)

    assert cargar(ruta) == PARES


def test_r5_guardar_produce_el_esquema_version_1(tmp_path):
    ruta = tmp_path / "notas.json"

    guardar(ruta, PARES)

    datos = json.loads(ruta.read_text(encoding="utf-8"))
    assert datos == {
        "version": 1,
        "notas": [
            {"nota": 4.0, "peso": 40.0},
            {"nota": 3.5, "peso": 60.0},
        ],
    }


def test_r5_version_distinta_lanza_value_error(tmp_path):
    ruta = tmp_path / "version_2.json"
    _escribir_json(
        ruta,
        {"version": 2, "notas": [{"nota": 4.0, "peso": 100.0}]},
    )

    with pytest.raises(ValueError):
        cargar(ruta)


def test_r5_falta_la_clave_peso_lanza_value_error(tmp_path):
    ruta = tmp_path / "sin_peso.json"
    _escribir_json(ruta, {"version": 1, "notas": [{"nota": 4.0}]})

    with pytest.raises(ValueError):
        cargar(ruta)


def test_r5_json_ilegible_lanza_value_error(tmp_path):
    ruta = tmp_path / "roto.json"
    ruta.write_text("{esto no es json", encoding="utf-8")

    with pytest.raises(ValueError):
        cargar(ruta)


def test_r5_guardar_valida_antes_de_escribir(tmp_path):
    ruta = tmp_path / "invalido.json"

    with pytest.raises(ValueError):
        guardar(ruta, [(6.0, 100.0)])

    assert not ruta.exists()


# R6: cargar un archivo inexistente es un error controlado.
def test_r6_cargar_archivo_inexistente_lanza_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        cargar(tmp_path / "no_existe.json")
