---
name: escribir-codigo
description: Implementa o corrige en src/ el contrato de docs/diseno.md con Python en capas, tipos y errores explícitos. Úsala para escribir código y también para leer código y citar archivo:línea.
---

# Escribir código

## Cuándo usarla

Al implementar o corregir los módulos descritos en `docs/diseno.md`. También sirve para leer el código existente y citar `archivo:línea` en un diagnóstico.

## Entrada y salida

- Entrada: el contrato y, si existe, el reporte de pruebas.
- Salida: módulos de `src/` que respetan las firmas y reglas del contrato.

## Orden de implementación por capas

1. Lógica pura: validación y cálculo. Sin entrada, salida, disco ni estado global.
2. Persistencia: guardar y cargar el formato acordado. Sin `print` ni `input`.
3. Presentación: pedir datos, mostrar resultados y capturar los errores de las capas anteriores.

## Reglas de estilo

- Python 3 con type hints en todas las funciones públicas.
- Nombres de módulos, funciones y parámetros exactamente como los fija el contrato.
- PEP 8: 4 espacios, líneas cortas, imports al inicio y sin imports sin usar.
- Sin constantes mágicas: nombra la tolerancia, la longitud mínima y el número de decimales.
- Errores explícitos: `ValueError` para validación y `FileNotFoundError` para archivo ausente. Nunca silencies una excepción ni la conviertas en un mensaje vacío.
- Docstring breve en cada función pública: qué recibe, qué devuelve y qué error lanza.
- La presentación no calcula y la lógica no imprime.

## Checklist de cierre

- [ ] Las firmas y los tipos de retorno coinciden con `docs/diseno.md`.
- [ ] Cada módulo se puede importar sin abrir la consola ni leer archivos: `py -c "import src.notas.core"` (ajusta el nombre si el contrato usa otro).
- [ ] No hay `print` ni `input` fuera del módulo de presentación.
- [ ] La validación cubre las reglas R1, R2 y R3 del contrato y lanza `ValueError`.
- [ ] El redondeo usa `Decimal` con `ROUND_HALF_UP` y dos decimales.
- [ ] `storage` usa utf-8 y distingue archivo inexistente (`FileNotFoundError`) de contenido inválido (`ValueError`).
- [ ] Si existe un reporte con reglas en `FALLA`, cada corrección apunta a la regla citada.

## Formato de salida

Al terminar, informa: archivos escritos, funciones implementadas, reglas cubiertas y cualquier desvío respecto del contrato. Si el contrato es ambiguo, no improvises una interfaz: señala la ambigüedad y detente.
