"""Pruebas de la logica pura: validacion y promedio (R1 a R4)."""

import pytest

from src.notas.calculos import promedio, suma_pesos, validar


# R1: cada nota esta en [0, 5].
def test_r1_limites_cero_y_cinco_son_validos():
    validar([(0.0, 50.0), (5.0, 50.0)])


def test_r1_nota_mayor_que_cinco_lanza_value_error():
    with pytest.raises(ValueError):
        validar([(5.1, 100.0)])


def test_r1_nota_negativa_lanza_value_error():
    with pytest.raises(ValueError):
        validar([(-0.1, 100.0)])


def test_r1_promedio_propaga_el_error_de_nota_fuera_de_rango():
    with pytest.raises(ValueError):
        promedio([(5.1, 100.0)])


# R2: los pesos suman 100 +- 0.01 y hay un peso por cada nota.
def test_r2_pesos_33_33_33_33_33_34_son_validos():
    validar([(4.0, 33.33), (4.0, 33.33), (4.0, 33.34)])


def test_r2_suma_90_lanza_value_error():
    with pytest.raises(ValueError):
        validar([(4.0, 60.0), (4.0, 30.0)])


def test_r2_suma_en_el_limite_de_tolerancia_es_valida():
    # 99.99 esta a exactamente 0.01 de 100.
    validar([(5.0, 50.0), (5.0, 49.99)])


def test_r2_suma_fuera_de_tolerancia_lanza_value_error():
    with pytest.raises(ValueError):
        validar([(5.0, 50.0), (5.0, 50.02)])


# R3: una lista vacia es error de validacion.
def test_r3_validar_lista_vacia_lanza_value_error():
    with pytest.raises(ValueError):
        validar([])


def test_r3_promedio_lista_vacia_lanza_value_error():
    with pytest.raises(ValueError):
        promedio([])


# R4: promedio ponderado redondeado a 2 decimales con mitad hacia arriba.
def test_r4_promedio_ponderado_basico():
    assert promedio([(4.0, 40.0), (3.5, 60.0)]) == 3.7


def test_r4_mitad_exacta_redondea_hacia_arriba():
    assert promedio([(4.005, 100.0)]) == 4.01


def test_r4_ejemplo_de_tres_pares():
    assert promedio([(4.0, 30.0), (3.5, 30.0), (5.0, 40.0)]) == 4.25


def test_r4_tercer_decimal_exacto_redondea_hacia_arriba():
    assert promedio([(3.835, 100.0)]) == 3.84


# Interfaz auxiliar: suma_pesos no valida, solo suma.
def test_suma_pesos_devuelve_la_suma_de_los_pesos():
    assert suma_pesos([(4.0, 40.0), (3.5, 60.0)]) == pytest.approx(100.0)
