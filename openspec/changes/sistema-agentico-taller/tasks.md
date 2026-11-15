# Tasks

## 1. Agentes y skills

- [ ] 1.1 Crear `.opencode/skills/disenar-programa/SKILL.md` con frontmatter `name` y `description`, pasos numerados, checklist de pensamiento computacional y plantilla de contrato; verificar que el archivo existe y que su `description` declara cuándo usarla.
- [ ] 1.2 Crear `.opencode/skills/escribir-codigo/SKILL.md` (estilo, tipos, orden por capas, checklist de cierre) y `.opencode/skills/generar-pruebas/SKILL.md` (una prueba por regla, `tmp_path`, plantilla de reporte, escalado a la segunda falla); verificar que ambas tienen frontmatter completo y pasos numerados.
- [ ] 1.3 Crear los tres agentes primarios en `.opencode/agents/` con solo `description` y `mode: primary`, indicando lectura, escritura, prohibiciones, skill que cargan y criterio de término según el diseño; verificar que ningún archivo usa `tools` ni `permission` de V1.
- [ ] 1.4 Verificar detección conjunta: `opencode agent list` muestra `arquitecto`, `programador` y `tester` como `primary`; `opencode debug skill` muestra `disenar-programa`, `escribir-codigo` y `generar-pruebas` con su ruta.
- [ ] 1.5 Verificar que no se tocaron las skills de OpenSpec: `git status --short .agents/skills` no muestra cambios y no se modificó nada en `~/.config/opencode/skills/`.

## 2. Contrato de diseño

- [ ] 2.1 Escribir `docs/diseno.md` con árbol de archivos, módulos, funciones con firmas y tipos de retorno, `ValueError` como error de validación, esquema JSON y reglas R1..R6 tal como están en `design.md`; verificar que cada regla tiene identificador y enunciado verificable.
- [ ] 2.2 Verificar el contrato contra `docs/idea.md`: cada regla de la idea (rango, suma de pesos, lista vacía, persistencia) aparece cubierta por al menos una regla R1..R6 y el contrato puede leerse sin abrir `src/`.

## 3. Código del programa

- [ ] 3.1 Implementar `src/notas/core.py` con la validación y el promedio ponderado según el contrato, usando `Decimal` con `ROUND_HALF_UP` para R4; verificar con una importación directa y un cálculo manual (4.0/30, 3.5/30, 5.0/40 -> 4.25).
- [ ] 3.2 Implementar `src/notas/storage.py` con guardar y cargar JSON en utf-8, `FileNotFoundError` para archivo inexistente y `ValueError` para contenido inválido; verificar guardando y cargando en una carpeta temporal fuera del repositorio.
- [ ] 3.3 Implementar `src/notas/cli.py` que pida notas y pesos, muestre el promedio con dos decimales y permita guardar y cargar, capturando `ValueError` sin traza y saliendo con código distinto de cero; verificar a mano un caso válido y uno inválido.

## 4. Pruebas y reporte

- [ ] 4.1 Escribir `tests/test_core.py` con una prueba por regla R1..R4, con nombres `test_rN_...`, incluyendo límites 0 y 5, el caso 33.33/33.33/33.34, lista vacía y el redondeo 3.835 -> 3.84; verificar que `py -m pytest -q tests/test_core.py` pasa.
- [ ] 4.2 Escribir `tests/test_storage.py` para R5 y R6 usando `tmp_path`, sin escribir JSON dentro del repositorio; verificar que `py -m pytest -q tests/test_storage.py` pasa y que `git status --short` no muestra archivos JSON nuevos.
- [ ] 4.3 Ejecutar `py -m pytest -q` desde la raíz y escribir `docs/reporte-pruebas.md` con el formato acordado (`Ronda: 1/2`, `Estado`, regla, esperado y obtenido); verificar que el reporte coincide con la salida real de pytest.
- [ ] 4.4 Verificar el tope del bucle: ante un fallo en la ronda 1, el Programador corrige y el Tester cierra en `Ronda: 2/2`; si la segunda vuelta falla, el reporte queda en `Estado: ESCALAR` y no existe `Ronda: 3/2` (usar una regla temporalmente incumplida y revertirla).

## 5. Integración y aceptación

- [ ] 5.1 Ejecutar el ciclo completo con sesiones nuevas (`opencode --agent arquitecto`, luego `programador`, luego `tester`) y verificar con `git status --short` después de cada rol que solo cambian los archivos del rol y que `docs/idea.md` queda igual.
- [ ] 5.2 Verificar los criterios de aceptación en una sola pasada: 3 agentes y 3 skills detectados, `py -m pytest -q` en verde, reporte con veredicto y sin tercera ronda, y ningún cambio en `opencode.json` ni en las skills de OpenSpec.
- [ ] 5.3 Escribir `README.md` de menos de una página con instalación de pytest, los tres comandos `opencode --agent`, el comando `py -m pytest -q` y el flujo resumido; verificar que cada comando del README funciona tal como está escrito.

## Workflow follow-up

- Revisar los artefactos del cambio con el usuario antes de implementar.
- Archivar el cambio después de que la aceptación esté verificada, si el usuario lo pide.
