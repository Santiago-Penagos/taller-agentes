# Taller de IA agéntica

Tres agentes de opencode y tres skills que diseñan, implementan y prueban, en sesiones separadas, una calculadora de notas ponderadas de consola. Los roles se comunican solo por archivos: `docs/idea.md` -> `docs/diseno.md` -> `src/` -> `docs/reporte-pruebas.md`.

## Requisitos

- opencode 1.19.5
- Python 3.14
- pytest 9

## Instalar pytest

```powershell
py -m pip install pytest
py -m pytest --version
```

## Los tres roles

Cada rol se inicia en su propia sesión y en ese orden. Sin `--agent`, opencode entra con el agente `plan`, que no escribe archivos.

```powershell
opencode --agent arquitecto
opencode --agent programador
opencode --agent tester
```

## Flujo

1. `arquitecto` lee `docs/idea.md` y escribe `docs/diseno.md` con capas, firmas, esquema JSON y reglas R1..R6.
2. `programador` lee `docs/diseno.md` y escribe el código en `src/`.
3. `tester` lee `docs/diseno.md`, escribe las pruebas en `tests/`, ejecuta pytest y emite `docs/reporte-pruebas.md` con `Ronda: 1/2`.
4. Si el reporte queda en `FALLA`, abre una sesión nueva de `programador` para corregir y otra de `tester` para la ronda 2. Si la ronda 2 falla, el estado es `ESCALAR` y no hay tercera vuelta.

## Ejecutar las pruebas

```powershell
py -m pytest -q
```
## Ejecutar el programa

Desde la raíz del repositorio:

```powershell
py -m src.main                       # pide notas y pesos por teclado
py -m src.main calcular [ARCHIVO]    # calcula desde un archivo JSON o por teclado
py -m src.main cargar ARCHIVO        # muestra las notas de un archivo JSON
py -m src.main guardar ARCHIVO       # pide notas y las guarda en JSON
py -m src.main ARCHIVO               # calcula desde un archivo JSON
py -m src.main ayuda                 # muestra la ayuda
```

## Estructura

- `.opencode/agents/`: `arquitecto.md`, `programador.md`, `tester.md`.
- `.opencode/skills/`: `disenar-programa`, `escribir-codigo`, `generar-pruebas`.
- `docs/idea.md`: reglas del programa, en solo lectura.
- Generados por los agentes: `docs/diseno.md`, `src/notas/`, `tests/` y `docs/reporte-pruebas.md`.
- `.agents/skills/`: skills propias de OpenSpec; no forman parte de las tres skills del taller.

## Cómo se planeó

El sistema se planeó con OpenSpec: la propuesta, las specs, el diseño y las tareas están en `openspec/changes/sistema-agentico-taller/`. Las tareas de agentes, skills y README las aplicó `/opsx-apply`; el contrato, el código y las pruebas los produjeron los propios agentes, cada uno en su sesión.