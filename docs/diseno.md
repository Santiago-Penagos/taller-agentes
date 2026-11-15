# Diseño: calculadora de notas ponderadas

## 1. Objetivo

Programa de consola en Python que calcula el promedio ponderado de una materia a partir de
pares nota-peso, y que puede guardar y cargar esas notas en un archivo JSON.

## 2. Capas y archivos

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Lógica pura | `src/notas/calculos.py` | Validar los pares nota-peso y calcular el promedio. Sin entrada, salida ni disco. |
| Persistencia | `src/notas/storage.py` | Leer y escribir el archivo JSON utf-8. Valida antes de guardar. |
| Presentación | `src/notas/presentacion.py` | Pedir datos, mostrar el resultado y convertir errores en mensajes y códigos de salida. |
| Paquete | `src/notas/__init__.py` | Marcador del paquete y constantes compartidas del formato. |
| Punto de entrada | `src/main.py` | Arranca `presentacion.main()` y devuelve su código de salida. |
| Pruebas | `tests/test_*.py` | Lo escribe el rol Tester; no lo define este contrato. |

Árbol:

```
src/
├── main.py
└── notas/
    ├── __init__.py
    ├── calculos.py
    ├── storage.py
    └── presentacion.py
tests/
└── test_*.py        # escrito por el Tester
```

Dirección de dependencias (sin ciclos): `main` -> `presentacion` -> {`calculos`, `storage`};
`storage` -> `calculos`; `calculos` no depende de nadie.

Constantes en `src/notas/__init__.py` (valores fijos, usados por las tres capas):

| Constante | Valor | Uso |
|---|---|---|
| `NOTA_MIN` | `0.0` | Cota inferior de cada nota (R1). |
| `NOTA_MAX` | `5.0` | Cota superior de cada nota (R1). |
| `PESO_TOTAL` | `100.0` | Suma esperada de los pesos (R2). |
| `TOLERANCIA_PESOS` | `0.01` | Tolerancia de la suma de pesos (R2). |
| `DECIMALES` | `2` | Decimales del promedio (R4). |
| `VERSION_ESQUEMA` | `1` | Campo `version` del JSON (R5). |

## 3. Interfaz pública

Tipo compartido: `ParNota = tuple[float, float]`, donde el primer elemento es la nota y el
segundo el peso. Nunca se usan listas paralelas.

| Módulo | Función | Firma | Retorno | Errores |
|---|---|---|---|---|
| `calculos` | `validar` | `validar(notas: Sequence[ParNota]) -> None` | `None` | `ValueError` si lista vacía (R3), nota fuera de [0, 5] (R1), peso fuera de [0, 100] (sin regla R propia, no se prueba), o pesos que no suman 100 +- 0.01 (R2) |
| `calculos` | `suma_pesos` | `suma_pesos(notas: Sequence[ParNota]) -> float` | suma de los pesos | ninguno (no valida) |
| `calculos` | `promedio` | `promedio(notas: Sequence[ParNota]) -> float` | promedio redondeado a 2 decimales | `ValueError` por `validar` (R1, R2, R3) |
| `storage` | `guardar` | `guardar(ruta: str \| Path, notas: Sequence[ParNota]) -> None` | `None` | `ValueError` si `validar` falla; `OSError` del sistema si no se puede escribir |
| `storage` | `cargar` | `cargar(ruta: str \| Path) -> list[ParNota]` | lista de pares nota-peso | `FileNotFoundError` si la ruta no existe (R6); `ValueError` si el JSON es ilegible o no respeta el esquema (R5) |
| `presentacion` | `formatear_promedio` | `formatear_promedio(valor: float) -> str` | texto con 2 decimales, p. ej. `"4.25"` | ninguno |
| `presentacion` | `main` | `main(argv: list[str] \| None = None) -> int` | código de salida: `0` ok, `1` error controlado, `2` uso incorrecto | no propaga; convierte `ValueError`, `FileNotFoundError` y `OSError` en mensaje y código |

Detalles de contrato que el Programador debe respetar:

- `calculos` no importa `storage` ni `presentacion`, y no imprime ni lee archivos.
- `storage` solo trata `str`/`Path` y nunca imprime.
- `presentacion` es el único módulo que escribe en pantalla y el único que llama a `sys.exit`.
- El texto exacto de los mensajes es libre; el tipo de excepción no.

## 4. Esquema JSON

Un objeto raíz con `version` y una lista `notas` de pares `nota`/`peso` (sin listas paralelas):

```json
{
  "version": 1,
  "notas": [
    { "nota": 4.0, "peso": 40.0 },
    { "nota": 3.5, "peso": 60.0 }
  ]
}
```

Reglas del formato (utf-8):

- `version` es un entero y debe ser igual a `VERSION_ESQUEMA`; otra versión es `ValueError`.
- `notas` es una lista; cada elemento es un objeto con las claves `nota` y `peso` numéricas.
- Falta una clave, sobra un tipo no numérico o el JSON no se puede decodificar: `ValueError`.
- `cargar` devuelve `[(4.0, 40.0), (3.5, 60.0)]` como `list[ParNota]`.
- `guardar` escribe con `encoding="utf-8"` y `ensure_ascii=False`, y produce exactamente esta
  forma; `cargar(guardar(x))` devuelve los mismos valores y la misma correspondencia nota-peso.

## 5. Reglas de aceptación

| Regla | Enunciado | Verificación esperada |
|---|---|---|
| R1 | Cada nota está en el rango [0, 5]; fuera de rango es error de validación. | `validar([(5.1, 100.0)])` y `validar([(-0.1, 100.0)])` lanzan `ValueError`; `validar([(0.0, 50.0), (5.0, 50.0)])` no lanza. |
| R2 | Los pesos suman 100 con tolerancia 0.01 y hay un peso por cada nota; si no, error de validación. | `validar([(4.0, 33.33), (4.0, 33.33), (4.0, 33.34)])` no lanza; `validar([(4.0, 60.0), (4.0, 30.0)])` lanza `ValueError` (suma 90). |
| R3 | Una lista vacía de notas es error de validación. | `validar([])` y `promedio([])` lanzan `ValueError`. |
| R4 | Promedio = suma(nota x peso) / 100, redondeado a 2 decimales con la mitad hacia arriba. | `promedio([(4.0, 40.0), (3.5, 60.0)]) == 3.7`; `promedio([(4.005, 100.0)]) == 4.01` (mitad hacia arriba). |
| R5 | Guardar y cargar en JSON utf-8 conserva los valores y la correspondencia nota-peso. | Tras `guardar(ruta, n)`, `cargar(ruta) == n` con `n = [(4.0, 40.0), (3.5, 60.0)]`; un JSON con `"version": 2` o sin la clave `peso` lanza `ValueError`. |
| R6 | Cargar un archivo inexistente es un error controlado. | `cargar("no_existe.json")` lanza `FileNotFoundError`; en `presentacion.main` ese caso no propaga y devuelve `1`. |

Algoritmo de R4, paso a paso (sin ambigüedad):

1. Llamar a `validar(notas)`; si falla, se propaga `ValueError`.
2. `suma = Decimal(0)`; para cada par, `suma += Decimal(str(nota)) * Decimal(str(peso))`.
3. `valor = suma / Decimal(str(PESO_TOTAL))`.
4. `redondeado = valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`.
5. Devolver `float(redondeado)`.

Se usa `Decimal` con `ROUND_HALF_UP` (mitad hacia arriba), no `round()` de Python.

## 6. Fuera de alcance

- Interfaz gráfica o web; solo consola.
- Más de una materia, historial, fechas o estadísticas.
- Formatos distintos de JSON (CSV, YAML, bases de datos).
- Migración entre versiones del esquema: solo se acepta `version` 1.
- Escribir en `docs/idea.md`, `src/` o `tests/`: fuera de las atribuciones del Arquitecto.

## 7. Convención de imports y ejecución

- Los módulos se importan siempre con el prefijo del repositorio, por ejemplo
  `from src.notas.calculos import validar`.
- Dentro de `src/notas/` se usan imports relativos (por ejemplo, `from .calculos import validar`).
- El programa se ejecuta con `py -m src.main` desde la raíz del repositorio.
- Las pruebas se ejecutan con `py -m pytest -q` desde la raíz del repositorio.
- No se requiere configuración extra de `sys.path`.
