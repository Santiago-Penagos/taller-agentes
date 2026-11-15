# Design

## Context

Ver `proposal.md` para la motivación. Restricciones que condicionan el diseño:

- opencode `1.19.5` instalado; lee frontmatter V2 de agentes (`permissions`) y traduce V1, pero mezclar ambos formatos descarta los campos V1. La ubicación preferida es `.opencode/agents/` y `.opencode/skills/<id>/SKILL.md`.
- El agente por defecto configurado es `plan`, que no edita archivos del proyecto. Por eso cada rol se lanza explícitamente con `opencode --agent <rol>`.
- Python `3.14.3` y pytest `9.2.0` disponibles. No se agregan dependencias.
- No se toca `opencode.json` (ni global ni de proyecto), ni `.agents/skills/`, ni `~/.config/opencode/skills/`.
- El repositorio no tiene código previo ni specs; solo `docs/idea.md` y OpenSpec inicializado.
- Entorno Windows con PowerShell; los comandos del README deben funcionar ahí.

## Goals / Non-Goals

**Goals:**

- Que `opencode agent list` y `opencode debug skill` detecten los 3 agentes y las 3 skills del taller.
- Que un ciclo completo Idea -> Arquitecto -> Programador -> Tester funcione con sesiones separadas y traspaso por archivos.
- Que el programa demo quede cubierto por pruebas deterministas y rápidas.
- Que el bucle de corrección tenga un estado escrito y un tope duro de 2 vueltas.

**Non-Goals:**

- Automatización del flujo (orquestador, subagentes, comandos `/rol`).
- Permisos finos por ruta como requisito; solo se evalúan si no rompen Windows.
- Pruebas de la CLI (se verifica a mano).
- Persistencia en base de datos, empaquetado, CI o interfaz gráfica.

## Decisions

### D1. Definiciones en Markdown bajo `.opencode/`, con frontmatter V2

- Agentes: `.opencode/agents/{arquitecto,programador,tester}.md` con `description` y `mode: primary`.
- Skills: `.opencode/skills/{disenar-programa,escribir-codigo,generar-pruebas}/SKILL.md` con `name` y `description`.
- Alternativas descartadas: `.opencode/agent/` y `mode/` (compatibilidad V1, no aportan nada); `.agents/skills/` (ya ocupado por OpenSpec y con precedencia más baja que `~/.config/opencode/skills`); agentes en JSON (menos didáctico y no pedido).
- No se usa `permission` ni `tools`. Si en el futuro se añaden permisos, será `permissions` con `{action, resource, effect}`.

### D2. Sin permisos por ruta en la primera versión

La propiedad de archivos se declara en el cuerpo del agente y se verifica con `git status --short` después de cada rol. Razón: en Windows los patrones de `resource` pueden no coincidir con la ruta real y producir denegaciones falsas durante la grabación. Si se quiere endurecer, se prueba primero un único caso (`deny edit *`, `allow edit docs/diseno.md`) y solo se incorpora si funciona; no bloquea el flujo.

### D3. Tres primarios manuales, una sesión por rol

El traspaso ocurre solo por archivos; cambiar de agente con Tab conserva el historial y rompería esa garantía. Comandos:

```text
opencode --agent arquitecto
opencode --agent programador
opencode --agent tester
```

El Programador puede repetirse una vez por vuelta de corrección, siempre en sesión nueva.

### D4. Contenido de los agentes (rol, no procedimiento)

Cada archivo contiene, en este orden:

| Agente | Lee | Escribe | No puede tocar | Skill que carga | Termina cuando |
|---|---|---|---|---|---|
| `arquitecto` | `docs/idea.md`, `docs/diseno.md` si existe | `docs/diseno.md` | `src/`, `tests/`, `docs/reporte-pruebas.md`, `docs/idea.md` | `disenar-programa` | El contrato tiene árbol, firmas, esquema JSON y R1..R6 completos |
| `programador` | `docs/diseno.md`, `docs/reporte-pruebas.md` si existe | `src/notas/*.py` | `docs/`, `tests/`, `docs/idea.md` | `escribir-codigo` | `src/` implementa el contrato o la corrección pedida |
| `tester` | `docs/diseno.md`, `docs/reporte-pruebas.md` si existe; `src/` solo para citar `archivo:línea` | `tests/*.py`, `docs/reporte-pruebas.md` | `src/`, `docs/diseno.md`, `docs/idea.md` | `generar-pruebas` y `escribir-codigo` | Reporte con `Estado: APROBADO` o `ESCALAR` |

Todos incluyen: prohibición explícita de modificar archivos de otro rol, instrucción de no pedir contexto conversacional y criterio de término. Los agentes no repiten los pasos de la skill.

### D5. Contenido de las skills (procedimiento reutilizable)

- `disenar-programa`: cuándo usarla; pasos numerados (leer `idea.md`, descomponer en capas, definir firmas, fijar esquema JSON, numerar R1..R6); checklist de pensamiento computacional (descomposición, patrón, abstracción, algoritmo, evaluación); plantilla de `docs/diseno.md` con secciones y tabla de reglas.
- `escribir-codigo`: cuándo usarla (Programador y Tester); reglas de estilo (PEP 8, type hints, sin efectos secundarios en `core`, sin `print` fuera de `cli`, errores explícitos); orden de implementación por capas; checklist de cierre (firmas coinciden con el contrato, no se tocaron archivos ajenos, se puede importar sin consola).
- `generar-pruebas`: cuándo usarla; pasos (leer contrato, una prueba por regla, valores límite y caso válido, nombres `test_rN_...`); uso de `tmp_path` para JSON; plantilla de `docs/reporte-pruebas.md` con `Ronda`, `Estado`, regla, esperado y obtenido; regla de escalado a la segunda falla.

La skill `escribir-codigo` se comparte a propósito para que el Tester pueda citar `archivo:línea` en un fallo, lo que justifica las skills como procedimientos y no como copias del agente.

### D6. Estructura del programa demo (KISS + capas)

```text
src/notas/core.py      # puro: validar() y promedio_ponderado(); ValueError
src/notas/storage.py   # guardar() y cargar(); JSON utf-8; FileNotFoundError/ValueError
src/notas/cli.py       # input/print, orquesta; captura ValueError y sale con código 1
tests/test_core.py
tests/test_storage.py
```

`core.py` no importa `storage` ni `cli`; `storage.py` no imprime; `cli.py` no calcula. `tests/` importa solo `core` y `storage`.

### D7. Contrato con interfaz fija y comportamiento en reglas

`docs/diseno.md` fija nombres, firmas, tipos de retorno, error esperado y el esquema JSON; el texto de los mensajes queda libre. Las reglas se numeran R1..R6:

| Regla | Comportamiento |
|---|---|
| R1 | Notas en [0, 5] |
| R2 | Pesos suman 100 con tolerancia 0.01 y coinciden en cantidad con las notas |
| R3 | Lista vacía es error |
| R4 | Promedio = suma(nota x peso) / 100, redondeo a 2 decimales con mitad hacia arriba |
| R5 | Guardar y cargar JSON utf-8 conservando pares nota-peso |
| R6 | Archivo inexistente es error controlado |

Supuestos registrados: `core` lanza `ValueError`; `storage.cargar` lanza `FileNotFoundError` si el archivo no existe y `ValueError` si el JSON no respeta el esquema. El redondeo se implementa con `Decimal` y `ROUND_HALF_UP` para evitar el redondeo bancario de `round()`.

### D8. Esquema JSON mínimo

```json
{"version": 1, "notas": [{"valor": 4.0, "peso": 30.0}]}
```

`guardar` escribe `version: 1`, `notas` y `peso`; `cargar` exige `notas` como lista de objetos con `valor` y `peso` numéricos. Campos extra se ignoran. Alternativa descartada: dos listas paralelas (más frágil ante desalineaciones).

### D9. Formato del reporte de pruebas

```text
Ronda: 1/2
Estado: FALLA

R2 - test_r2_pesos_suman_100_con_tolerancia
Esperado: aceptar 33.33 + 33.33 + 33.34
Obtenido: ValueError: los pesos deben sumar 100
```

Solo el Tester crea o modifica el archivo, incrementa la ronda y escribe el veredicto. `APROBADO` cierra el ciclo; `ESCALAR` aparece únicamente en `Ronda: 2/2`.

### D10. Verificación del entorno sin depender de la intuición

| Verificación | Comando | Resultado esperado |
|---|---|---|
| Agentes detectados | `opencode agent list` | `arquitecto`, `programador`, `tester` en `primary` |
| Skills detectadas | `opencode debug skill` | las 3 skills del taller con su ruta |
| Pruebas | `py -m pytest -q` | todas pasan, sin escribir JSON en el repo |
| Propiedad | `git status --short` tras cada rol | solo archivos del rol |

## Risks / Trade-offs

- **[El modelo acierta a la primera y no hay bucle]** -> R2 con tolerancia 0.01 y decimales 33.33/33.34 producen un fallo realista (comparación de floats con `==`); conviene ensayar y, si acierta, dejar la regla como está y mostrar la ronda 1 en verde sin inventar fallos.
- **[Tab en la misma sesión filtra contexto]** -> prohibido por diseño; cada rol se lanza con `--agent` en sesión nueva.
- **[El default `plan` confunde al operador]** -> README y video usan siempre `--agent`; no se modifica `opencode.json`.
- **[Permisos por ruta fallan en Windows]** -> no se usan; la propiedad se verifica con `git status`.
- **[Pruebas acopladas a la implementación]** -> el Tester trabaja desde el contrato y el contrato fija la interfaz, no la implementación.
- **[Redondeo ambiguo]** -> mitad hacia arriba explícita en R4 y en el contrato; los tests usan valores con tercer decimal inequívoco.
- **[JSON de prueba contamina el repo]** -> `tmp_path` obligatorio; `guardar` recibe la ruta como argumento.
- **[Video de 5 minutos sobrecargado]** -> el diseño deja la CLI fuera de las pruebas y permite mostrar solo R2 y una corrección; los cortes cubren el resto.
- **[Skills cargadas a medias]** -> cada agente pide explícitamente su skill y la skill contiene el checklist y la plantilla, no el rol.

## Migration Plan

Proyecto nuevo, sin migración de datos ni de specs. El orden de aplicación es: definiciones y skills, contrato, código, pruebas y reporte, README. Rollback: eliminar los archivos creados por el cambio; no hay specs principales sincronizadas hasta archivar el cambio.

## Open Questions

- Si el video lo permite, ¿se añade una demostración de permisos V2 por ruta como extra, después de validarlos en Windows?
- ¿Se conserva `version: 1` en el JSON en el futuro o se elimina para simplificar aún más?
