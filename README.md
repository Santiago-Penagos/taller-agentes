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

## Estructura

- `.opencode/agents/`: `arquitecto.md`, `programador.md`, `tester.md`.
- `.opencode/skills/`: `disenar-programa`, `escribir-codigo`, `generar-pruebas`.
- `docs/idea.md`: reglas del programa, en solo lectura.
- Generados por los agentes: `docs/diseno.md`, `src/notas/`, `tests/` y `docs/reporte-pruebas.md`.
