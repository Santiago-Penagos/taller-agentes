# Spec Delta

## Purpose

Define un flujo de trabajo agéntico de tres roles que diseñan, implementan y prueban un programa, comunicándose únicamente mediante archivos y con un bucle de corrección acotado.

## ADDED Requirements

### Requirement: Detección de roles y procedimientos del taller
opencode DEBE detectar los tres agentes del taller y las tres skills del taller desde el repositorio, sin configuración global adicional.

#### Scenario: Listado de agentes
- **WHEN** se ejecuta `opencode agent list` en la raíz del repositorio
- **THEN** aparecen `arquitecto`, `programador` y `tester` en modo `primary`

#### Scenario: Detección de skills
- **WHEN** se ejecuta `opencode debug skill` en la raíz del repositorio
- **THEN** aparecen las skills `disenar-programa`, `escribir-codigo` y `generar-pruebas`

#### Scenario: Skills ajenas intactas
- **WHEN** se inspeccionan las skills del taller
- **THEN** ninguna de las skills de OpenSpec en `.agents/skills` o `~/.config/opencode/skills` fue modificada

### Requirement: Invocación manual en sesión separada
Cada rol DEBE iniciarse manualmente en una sesión nueva de opencode; el flujo no DEBE depender de orquestación automática, subagentes ni cambios de agente dentro de una sesión.

#### Scenario: Inicio de un rol
- **WHEN** se ejecuta `opencode --agent arquitecto` en la raíz del repositorio
- **THEN** la sesión se inicia con el rol Arquitecto y su primera acción es leer `docs/idea.md`

#### Scenario: Cambio de rol sin arrastre de contexto
- **WHEN** termina un rol y se inicia el siguiente con `opencode --agent <rol>`
- **THEN** el nuevo rol obtiene su contexto leyendo archivos del repositorio, no de la conversación anterior

### Requirement: Propiedad exclusiva de archivos
Cada rol DEBE escribir únicamente en los archivos de su propiedad y DEBE tratar `docs/idea.md` como solo lectura.

#### Scenario: Propiedad del Arquitecto
- **WHEN** el Arquitecto completa su trabajo
- **THEN** el único archivo nuevo o modificado es `docs/diseno.md`

#### Scenario: Propiedad del Programador
- **WHEN** el Programador completa su trabajo
- **THEN** los únicos archivos nuevos o modificados están bajo `src/`

#### Scenario: Propiedad del Tester
- **WHEN** el Tester completa su trabajo
- **THEN** los únicos archivos nuevos o modificados están bajo `tests/` y en `docs/reporte-pruebas.md`, y ningún archivo bajo `src/` cambió

#### Scenario: Idea inmutable
- **WHEN** cualquier rol termina su trabajo
- **THEN** `docs/idea.md` conserva su contenido original

### Requirement: Traspaso de trabajo mediante archivos
Los roles DEBEN comunicarse exclusivamente mediante archivos del repositorio: `docs/idea.md`, `docs/diseno.md` y `docs/reporte-pruebas.md`.

#### Scenario: Programador guiado por el contrato
- **WHEN** el Programador inicia en una sesión nueva
- **THEN** lee `docs/diseno.md` y escribe el código en `src/` conforme a ese contrato

#### Scenario: Tester guiado por el contrato
- **WHEN** el Tester inicia en una sesión nueva
- **THEN** diseña las pruebas a partir de `docs/diseno.md` y no a partir de leer `src/`

#### Scenario: Nombres de prueba ligados a reglas
- **WHEN** el Tester escribe una prueba para una regla de aceptación
- **THEN** el nombre de la prueba incluye el identificador de la regla, por ejemplo `test_r2_pesos_suman_100_con_tolerancia`

### Requirement: Bucle de corrección acotado a dos vueltas
El flujo DEBE permitir como máximo dos vueltas de corrección; solo el Tester DEBE incrementar la ronda y emitir el veredicto en `docs/reporte-pruebas.md`.

#### Scenario: Primera vuelta con fallo
- **WHEN** una prueba falla en la ronda 1
- **THEN** el reporte queda con `Ronda: 1/2` y `Estado: FALLA`, indicando la regla rota y el resultado esperado frente al obtenido

#### Scenario: Corrección exitosa
- **WHEN** el Programador corrige `src/` y el Tester vuelve a ejecutar las pruebas en la ronda 2
- **THEN** el reporte queda con `Ronda: 2/2` y `Estado: APROBADO`

#### Scenario: Segunda vuelta con fallo
- **WHEN** una prueba vuelve a fallar en la ronda 2
- **THEN** el reporte queda con `Estado: ESCALAR` y el Tester se detiene sin iniciar una tercera vuelta

### Requirement: Separación entre rol y procedimiento
Cada agente DEBE contener solo su rol, archivos que posee, prohibiciones y criterio de término, y DEBE indicar explícitamente qué skill carga; cada skill DEBE contener el procedimiento, checklist o plantilla, sin duplicar el rol.

#### Scenario: Skill declarada
- **WHEN** se lee la definición de un agente del taller
- **THEN** incluye una instrucción explícita de cargar su skill correspondiente

#### Scenario: Procedimiento reutilizable
- **WHEN** se lee una skill del taller
- **THEN** contiene pasos numerados y una plantilla o checklist, y no repite las prohibiciones ni la propiedad de archivos del agente
