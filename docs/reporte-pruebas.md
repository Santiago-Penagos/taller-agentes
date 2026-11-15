# Reporte de pruebas

Ronda: 2/2
Estado: APROBADO

## Resultado de pytest

```
..........................                                               [100%]
26 passed in 0.14s
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
| R4 | test_r4_mitad_exacta_redondea_hacia_arriba | PASA |
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

Ninguno en esta ronda.

El único fallo de la ronda 1 (R4, `test_r4_mitad_exacta_redondea_hacia_arriba`, obtenido
`4.0` en vez de `4.01`) quedó corregido: `src/notas/calculos.py:103` ahora aplica
`valor.quantize(_CUANTIZADOR, rounding=ROUND_HALF_UP)`.

## Observaciones

- Las pruebas no cambiaron entre rondas: se mantienen las mismas 26 pruebas de la ronda 1,
  ejecutadas contra el código corregido.
- R6 en `presentacion.main`: el contrato no fija la sintaxis de `argv`. La prueba usa la
  forma documentada por el programa (`main(["cargar", RUTA])`) para llegar a la carga de un
  archivo inexistente y comprobar que devuelve `1` sin propagar. Si el Programador cambiara
  esa sintaxis, habría que revisar esta prueba junto con el contrato.
- `git status --short` no muestra archivos JSON nuevos: todas las pruebas de persistencia usan
  `tmp_path`.

## Veredicto

APROBADO: R1, R2, R3, R4, R5 y R6 se cumplen y las 26 pruebas pasan. No hay correcciones
pendientes para el Programador.
