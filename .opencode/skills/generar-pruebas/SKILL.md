---
name: generar-pruebas
description: Diseña pruebas pytest desde las reglas de docs/diseno.md, las ejecuta y produce docs/reporte-pruebas.md con ronda y veredicto. Úsala para probar el programa sin leer su implementación.
---

# Generar pruebas

## Cuándo usarla

Al probar el programa descrito en `docs/diseno.md` o al repetir la ejecución después de una corrección. Las pruebas se diseñan desde el contrato; el código fuente solo se consulta para citar `archivo:línea` en un fallo.

## Entrada y salida

- Entrada: `docs/diseno.md` y el reporte anterior si existe.
- Salida: archivos de `tests/` y `docs/reporte-pruebas.md`.

## Pasos

1. Lee `docs/diseno.md` completo y extrae las firmas, el esquema JSON y las reglas R1..R6.
2. Asigna al menos una prueba por regla. El nombre debe incluir el identificador: `test_r1_...`, `test_r2_...`, hasta `test_r6_...`.
3. Para cada regla, cubre un caso válido, los límites y al menos un caso inválido:
   - R1: notas 0 y 5 válidas; nota negativa y nota mayor que 5 lanzan `ValueError`.
   - R2: pesos 33.33, 33.33 y 33.34 se aceptan; una suma fuera de la tolerancia 0.01 lanza `ValueError`; longitudes distintas lanzan `ValueError`.
   - R3: lista vacía lanza `ValueError`.
   - R4: 4.0/30, 3.5/30 y 5.0/40 dan 4.25; un tercer decimal exacto como 3.835 se redondea a 3.84.
   - R5: guardar y cargar en un archivo temporal conserva los pares nota-peso.
   - R6: un archivo inexistente lanza `FileNotFoundError`; un JSON que no respeta el esquema lanza `ValueError`.
4. Usa `tmp_path` de pytest para todo archivo de datos. No escribas JSON dentro del repositorio.
5. Ejecuta `py -m pytest -q` desde la raíz y registra la salida real.
6. Escribe `docs/reporte-pruebas.md` con la plantilla.
7. Si falla una regla en la ronda 1, deja el estado en `FALLA` para que el Programador corrija. Al repetir, usa la ronda 2. Si vuelve a fallar, escribe `ESCALAR` y detente.

## Regla de ronda

| Situación | Ronda y estado |
|---|---|
| Primera ejecución con fallos | `Ronda: 1/2`, `Estado: FALLA` |
| Segunda ejecución correcta | `Ronda: 2/2`, `Estado: APROBADO` |
| Segunda ejecución con fallos | `Ronda: 2/2`, `Estado: ESCALAR` |
| Ejecución correcta a la primera | `Ronda: 1/2`, `Estado: APROBADO` |

Nunca existe una tercera ronda.

## Plantilla de docs/reporte-pruebas.md

```markdown
# Reporte de pruebas

Ronda: 1/2
Estado: FALLA

## Resultado de pytest

<resumen real de py -m pytest -q>

## Reglas

| Regla | Prueba | Resultado |
|---|---|---|
| R1 | test_r1_... | PASA |
| R2 | test_r2_... | FALLA |

## Fallos

### R2 - test_r2_pesos_suman_100_con_tolerancia
- Esperado: aceptar 33.33 + 33.33 + 33.34
- Obtenido: ValueError: los pesos deben sumar 100
- Ubicación: src/notas/core.py:37

## Veredicto

FALLA: el Programador debe corregir las reglas listadas. / APROBADO: no hay correcciones pendientes. / ESCALAR: segunda vuelta con fallos, requiere intervención humana.
```

## Checklist de cierre

- [ ] Cada regla R1..R6 tiene al menos una prueba y su nombre incluye el identificador.
- [ ] Hay casos válidos, límites e inválidos para cada regla.
- [ ] `tests/test_storage.py` usa `tmp_path` y `git status --short` no muestra archivos JSON nuevos.
- [ ] `py -m pytest -q` se ejecutó y el reporte reproduce su salida real.
- [ ] El reporte declara ronda y veredicto, con esperado y obtenido en cada fallo.
- [ ] No hay una tercera ronda: a la segunda falla el estado es `ESCALAR`.

## Formato de salida

Al terminar, informa: pruebas escritas, resultado por regla, ronda y veredicto.
