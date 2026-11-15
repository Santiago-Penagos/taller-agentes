# Reporte de pruebas

Ronda: 1/2
Estado: FALLA

## Resultado de pytest

```
...........F..............                                               [100%]
================================== FAILURES ===================================
_________________ test_r4_mitad_exacta_redondea_hacia_arriba __________________

    def test_r4_mitad_exacta_redondea_hacia_arriba():
>       assert promedio([(4.005, 100.0)]) == 4.01
E       assert 4.0 == 4.01
E        +  where 4.0 = promedio([(4.005, 100.0)])

tests\test_calculos.py:65: AssertionError
=========================== short test summary info ============================
FAILED tests/test_calculos.py::test_r4_mitad_exacta_redondea_hacia_arriba - a...
1 failed, 25 passed in 0.25s
```

## Reglas

| Regla | Prueba | Resultado |
|---|---|---|
| R1 | test_r1_limites_cero_y_cinco_son_validos | PASA |
| R1 | test_r1_nota_mayor_que_cinco_lanza_value_error | PASA |
| R1 | test_r1_nota_negativa_lanza_value_error | PASA |
| R1 | test_r1_promedio_propaga_el_error_de_nota_fuera_de_rango | PASA |
| R2 | test_r2_pesos_33_33_33_33_33_34_son_validos | PASA |
| R2 | test_r2_suma_90_lanza_value_error | PASA |
| R2 | test_r2_suma_en_el_limite_de_tolerancia_es_valida | PASA |
| R2 | test_r2_suma_fuera_de_tolerancia_lanza_value_error | PASA |
| R3 | test_r3_validar_lista_vacia_lanza_value_error | PASA |
| R3 | test_r3_promedio_lista_vacia_lanza_value_error | PASA |
| R4 | test_r4_promedio_ponderado_basico | PASA |
| R4 | test_r4_mitad_exacta_redondea_hacia_arriba | FALLA |
| R4 | test_r4_ejemplo_de_tres_pares | PASA |
| R4 | test_r4_tercer_decimal_exacto_redondea_hacia_arriba | PASA |
| R5 | test_r5_guardar_y_cargar_conserva_los_pares | PASA |
| R5 | test_r5_guardar_produce_el_esquema_version_1 | PASA |
| R5 | test_r5_version_distinta_lanza_value_error | PASA |
| R5 | test_r5_falta_la_clave_peso_lanza_value_error | PASA |
| R5 | test_r5_json_ilegible_lanza_value_error | PASA |
| R5 | test_r5_guardar_valida_antes_de_escribir | PASA |
| R6 | test_r6_cargar_archivo_inexistente_lanza_file_not_found | PASA |
| R6 | test_r6_main_con_archivo_inexistente_devuelve_1_sin_propagar | PASA |
| Interfaz | test_suma_pesos_devuelve_la_suma_de_los_pesos | PASA |
| Interfaz | test_formatear_promedio_usa_dos_decimales | PASA |
| Interfaz | test_main_con_json_invalido_devuelve_1_sin_propagar | PASA |
| Interfaz | test_main_con_uso_incorrecto_devuelve_2 | PASA |

## Fallos

### R4 - test_r4_mitad_exacta_redondea_hacia_arriba

- Esperado: `promedio([(4.005, 100.0)]) == 4.01` (mitad hacia arriba).
- Obtenido: `4.0`, porque la mitad exacta se redondea hacia el par y no hacia arriba.
- Ubicación: `src/notas/calculos.py:103`. La llamada `valor.quantize(_CUANTIZADOR)`
  omite `rounding=ROUND_HALF_UP`, así que usa el modo por defecto del contexto
  (`ROUND_HALF_EVEN`). `ROUND_HALF_UP` sí está importado en `src/notas/calculos.py:8`,
  pero no se aplica.

## Observaciones

- R6 en `presentacion.main`: el contrato no fija la sintaxis de `argv`. La prueba usa la
  forma documentada por el programa (`main(["cargar", RUTA])`) para llegar a la carga de un
  archivo inexistente y comprobar que devuelve `1` sin propagar. Si el Programador cambiara
  esa sintaxis, habría que revisar esta prueba junto con el contrato.

## Veredicto

FALLA: el Programador debe corregir R4 en `promedio` para redondear con `Decimal` y
`ROUND_HALF_UP` a 2 decimales. R1, R2, R3, R5 y R6 se aprueban en esta ronda.
