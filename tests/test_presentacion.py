"""Pruebas de presentacion: formato y codigos de salida (R6 en main)."""

from src.notas.presentacion import formatear_promedio, main


def test_formatear_promedio_usa_dos_decimales():
    assert formatear_promedio(4.25) == "4.25"


def test_r6_main_con_archivo_inexistente_devuelve_1_sin_propagar(tmp_path):
    # El contrato no fija la sintaxis de argv; se usa la forma documentada
    # "cargar RUTA" para ejercitar la lectura de un archivo.
    ruta = tmp_path / "no_existe.json"

    codigo = main(["cargar", str(ruta)])

    assert codigo == 1


def test_main_con_json_invalido_devuelve_1_sin_propagar(tmp_path):
    ruta = tmp_path / "version_2.json"
    ruta.write_text(
        '{"version": 2, "notas": [{"nota": 4.0, "peso": 100.0}]}',
        encoding="utf-8",
    )

    codigo = main(["cargar", str(ruta)])

    assert codigo == 1


def test_main_con_uso_incorrecto_devuelve_2(capsys):
    codigo = main(["cargar"])

    assert codigo == 2
    assert capsys.readouterr().out
