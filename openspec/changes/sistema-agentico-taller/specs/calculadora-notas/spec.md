# Spec Delta

## Purpose

Define el comportamiento de una calculadora de consola que valida notas y pesos, calcula el promedio ponderado y persiste los datos en JSON.

## ADDED Requirements

### Requirement: Notas dentro del rango permitido
Cada nota DEBE ser un número entre 0 y 5 inclusive; cualquier nota fuera de ese rango DEBE producir un `ValueError`.

#### Scenario: Nota en el límite inferior
- **WHEN** se calcula un promedio que incluye la nota 0
- **THEN** la nota se acepta

#### Scenario: Nota en el límite superior
- **WHEN** se calcula un promedio que incluye la nota 5
- **THEN** la nota se acepta

#### Scenario: Nota negativa
- **WHEN** se calcula un promedio que incluye una nota menor que 0
- **THEN** se lanza `ValueError`

#### Scenario: Nota mayor que cinco
- **WHEN** se calcula un promedio que incluye una nota mayor que 5
- **THEN** se lanza `ValueError`

### Requirement: Pesos válidos y correspondencia con las notas
Los pesos DEBEN sumar 100 con una tolerancia de 0.01 y DEBE existir un peso por cada nota; cualquier incumplimiento DEBE producir un `ValueError`.

#### Scenario: Pesos con decimales que suman cien
- **WHEN** se usan los pesos 33.33, 33.33 y 33.34
- **THEN** los pesos se aceptan por estar dentro de la tolerancia

#### Scenario: Pesos que no suman cien
- **WHEN** la suma de los pesos difiere de 100 en más de 0.01
- **THEN** se lanza `ValueError`

#### Scenario: Cantidad de pesos distinta de la cantidad de notas
- **WHEN** se recibe una lista de notas y otra de pesos con longitudes diferentes
- **THEN** se lanza `ValueError`

### Requirement: Lista de notas vacía es inválida
Una lista vacía de notas DEBE considerarse un error de validación con `ValueError`.

#### Scenario: Sin notas
- **WHEN** se calcula el promedio de una lista vacía
- **THEN** se lanza `ValueError`

### Requirement: Promedio ponderado con redondeo a dos decimales
El promedio DEBE calcularse como la suma de cada nota multiplicada por su peso, dividida entre 100, y DEBE redondearse a dos decimales con la mitad hacia arriba.

#### Scenario: Promedio exacto
- **WHEN** se calculan las notas 4.0 con peso 30, 3.5 con peso 30 y 5.0 con peso 40
- **THEN** el resultado es 4.25

#### Scenario: Redondeo de la mitad hacia arriba
- **WHEN** el promedio sin redondear termina en 0.005 o más en el tercer decimal
- **THEN** el segundo decimal aumenta en una unidad, por ejemplo 3.835 se redondea a 3.84

### Requirement: Persistencia en JSON
El sistema DEBE guardar y cargar notas y pesos en un archivo JSON codificado en UTF-8, conservando los valores y la correspondencia entre nota y peso.

#### Scenario: Guardar y volver a cargar
- **WHEN** se guardan notas y pesos válidos y luego se cargan desde el mismo archivo
- **THEN** los valores y su correspondencia coinciden con los originales

#### Scenario: Archivo inexistente
- **WHEN** se intenta cargar un archivo que no existe
- **THEN** se lanza `FileNotFoundError`

#### Scenario: Contenido no interpretable como JSON
- **WHEN** se intenta cargar un archivo con contenido que no es JSON válido para este esquema
- **THEN** se lanza `ValueError`

### Requirement: Consola delgada con manejo de errores
La interfaz de consola DEBE solicitar notas y pesos, mostrar el promedio con dos decimales y ofrecer guardar y cargar; ante un error de validación DEBE mostrar el mensaje sin traza de error y terminar con código distinto de cero.

#### Scenario: Cálculo exitoso en consola
- **WHEN** el usuario ingresa notas y pesos válidos
- **THEN** la consola muestra el promedio con dos decimales

#### Scenario: Entrada inválida en consola
- **WHEN** el usuario ingresa datos que violan una regla de aceptación
- **THEN** la consola muestra el mensaje de error y termina con código distinto de cero

### Requirement: Separación en capas
La lógica de validación y cálculo DEBE ser independiente de la consola y del disco, y la persistencia DEBE ser independiente de la presentación.

#### Scenario: Lógica sin entrada ni salida
- **WHEN** se importa y ejecuta la lógica de cálculo en una prueba
- **THEN** no requiere entrada por teclado, ni imprime, ni accede al sistema de archivos

#### Scenario: Persistencia sin consola
- **WHEN** se guardan o cargan datos en una prueba
- **THEN** la operación no imprime ni solicita datos por teclado
