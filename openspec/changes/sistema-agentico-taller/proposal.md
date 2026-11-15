# Proposal

## Why

El taller exige demostrar un sistema de IA agéntica con al menos 3 agentes y 3 skills que diseñen, implementen y prueben un programa. Hoy el repositorio solo contiene la idea del programa (`docs/idea.md`): no hay agentes, skills, contrato de diseño, código ni pruebas. Hace falta un flujo mínimo, reproducible y demostrable en un video de 5 minutos, con roles separados y comunicación exclusivamente por archivos.

## What Changes

- **Flujo de tres roles primarios** invocados manualmente, cada uno en una sesión nueva: Arquitecto -> Programador -> Tester. Sin orquestador, sin subagentes y sin cambiar de agente dentro de una sesión.
- **Tres agentes** en `.opencode/agents/`: `arquitecto.md`, `programador.md`, `tester.md`, con frontmatter `description` y `mode: primary`.
- **Tres skills** en `.opencode/skills/`: `disenar-programa`, `escribir-codigo`, `generar-pruebas`, con frontmatter `name` y `description`. Cada agente declara explícitamente qué skill carga.
- **Contrato en `docs/diseno.md`**: dueño el Arquitecto; fija árbol de archivos, módulos, funciones con firmas y retorno, `ValueError` como error de validación, esquema JSON y reglas de aceptación numeradas R1..R6.
- **Programa de demostración en capas**: `src/notas/core.py` (lógica pura), `src/notas/storage.py` (JSON en utf-8) y `src/notas/cli.py` (entrada/salida).
- **Pruebas pytest** en `tests/test_core.py` y `tests/test_storage.py`, diseñadas desde el contrato y nombradas por regla; `test_storage.py` usa `tmp_path`.
- **Bucle de corrección acotado a 2 vueltas**, con estado en `docs/reporte-pruebas.md` (`Ronda: n/2`, `Estado: FALLA/APROBADO/ESCALAR`). Solo el Tester incrementa la ronda y emite el veredicto.
- **Propiedad exclusiva de archivos**: Arquitecto escribe `docs/diseno.md`; Programador escribe `src/`; Tester escribe `tests/` y `docs/reporte-pruebas.md`; `docs/idea.md` es solo lectura para todos.
- **README de una página** con instalación de pytest, lanzamiento de cada rol y ejecución de pruebas.
- **Sin** `opencode.json` propio, comandos personalizados, hooks, MCP, orquestador, subagentes, interfaz gráfica, base de datos, frameworks web ni modelos distintos por agente.

## Capabilities

### New Capabilities
- `flujo-agentico`: definición y detección por opencode de tres agentes y tres skills, propiedad exclusiva de archivos, secuencia de traspaso mediante archivos y bucle de corrección acotado a dos vueltas.
- `calculadora-notas`: comportamiento del programa de consola: validación de notas y pesos, cálculo del promedio ponderado con redondeo, persistencia JSON y manejo de archivo inexistente.

### Modified Capabilities
- Ninguna. El proyecto no tiene specs previas.

## Impact

- Archivos nuevos: `.opencode/agents/*.md`, `.opencode/skills/*/SKILL.md`, `docs/diseno.md`, `src/notas/*.py`, `tests/*.py`, `README.md`.
- Dependencias: Python 3.14 y pytest 9.2 ya instalados en este entorno; no se agregan dependencias externas.
- No se modifican `docs/idea.md`, `opencode.json` ni las skills de OpenSpec en `.agents/skills/` y `~/.config/opencode/skills/`.
- Cambio acotado al repo local; sin impacto en otros proyectos ni en la configuración global de opencode.
