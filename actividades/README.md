# Actividades de Python

## Actividad 1: Lista de números y estadísticas básicas

## Objetivo

Crear y manipular una lista y calcular su suma y promedio.

## Operaciones realizadas

1. Se crea `números` con `[10, 20, 30, 40, 50]`.
2. `append(60)` añade 60 al final.
3. `insert(1, 15)` coloca 15 entre 10 y 20.
4. `remove(30)` elimina el valor 30.
5. `sum(números)` calcula el total y lo guarda en `suma`.
6. `suma / len(números)` calcula la media y la guarda en `promedio`.
7. Se imprimen la lista resultante, la suma y el promedio.

## Ejecución

Requiere Python 3, sin dependencias externas. Desde la raíz del repositorio:

```powershell
python actividades/lista_numeros.py
```

## Resultado esperado

```text
Lista resultante: [10, 15, 20, 40, 50, 60]
Suma: 195
Promedio: 32.5
```

## Actividad 2: Tuplas de contacto

El archivo `tuplas_contacto.py` crea la tupla `contacto` con el nombre, correo y teléfono de Ana García, en ese orden. La desempaqueta en `nombre`, `email` y `telefono`, e imprime cada variable en una línea separada.

Después crea `contacto_completo` mediante `contacto + ("Madrid",)`. Como las tuplas son inmutables, esta operación crea una tupla nueva y conserva la original. La coma en `("Madrid",)` es necesaria para representar una tupla de un solo elemento.

Desde la raíz del repositorio:

```powershell
python actividades/tuplas_contacto.py
```

Resultado esperado:

```text
Ana García
ana@ejemplo.com
555-1234
Contacto completo: ('Ana García', 'ana@ejemplo.com', '555-1234', 'Madrid')
```

## Actividad 3: Diccionarios de contactos

El archivo `diccionarios_contactos.py` crea `contactos` con tres personas: Ana, Luis y Marta. Cada clave identifica un contacto y contiene otro diccionario con `nombre`, `telefono` y `email`. Los teléfonos se almacenan como texto porque son identificadores, no cantidades para calcular.

Operaciones realizadas:

1. Accede a `contactos["persona2"]["email"]` y muestra el correo de Luis, la segunda persona añadida.
2. Añade a Carlos con la clave `persona4`.
3. Cambia el teléfono de Ana mediante `contactos["persona1"]["telefono"]`.
4. Recorre `contactos.values()` con un bucle y muestra los nombres de los cuatro contactos.

Desde la raíz del repositorio:

```powershell
python actividades/diccionarios_contactos.py
```

Resultado esperado:

```text
Correo de la segunda persona: luis@ejemplo.com
Teléfono actualizado de Ana: 987654321
Nombres de los contactos:
Ana
Luis
Marta
Carlos
```

## Actividad 4: Operaciones con conjuntos

El archivo `conjuntos_numeros.py` convierte `lista1 = [1, 2, 3, 4, 5, 6]` y `lista2 = [4, 5, 6, 7, 8, 9]` en conjuntos mediante `set()`.

- `conjunto1 & conjunto2`: intersección, los elementos presentes en ambas listas.
- `conjunto1 - conjunto2`: elementos exclusivos de la primera lista.
- `conjunto2 - conjunto1`: elementos exclusivos de la segunda lista.
- `conjunto1 | conjunto2`: unión, todos los elementos sin duplicados.

Los resultados se almacenan como conjuntos. Como los conjuntos no garantizan un orden de presentación, se utiliza `sorted()` únicamente al imprimir para mostrarlos ordenados.

Desde la raíz del repositorio:

```powershell
python actividades/conjuntos_numeros.py
```

Resultado esperado:

```text
Intersección: [4, 5, 6]
Solo en la primera lista: [1, 2, 3]
Solo en la segunda lista: [7, 8, 9]
Unión: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Actividad 5: Frecuencias de caracteres con Counter

El archivo `analisis_texto_counter.py` implementa `analizar_texto(texto)`. Utiliza `Counter` del módulo estándar `collections` para contar caracteres y devuelve un diccionario con:

- `caracteres_mas_comunes`: lista de hasta tres tuplas `(caracter, frecuencia)`, obtenida con `most_common(3)` sin contar espacios en blanco.
- `total_caracteres`: longitud del texto original, incluyendo espacios.
- `total_sin_espacios`: cantidad de caracteres que no son espacios en blanco.

Se utiliza `isspace()` para excluir también tabulaciones y saltos de línea. Se distinguen mayúsculas de minúsculas y se cuentan los signos de puntuación. En empates de frecuencia, `Counter` conserva el orden de primera aparición. Si el texto está vacío, devuelve una lista vacía y ambos totales en cero; si hay menos de tres caracteres distintos, devuelve los disponibles.

Desde la raíz del repositorio, sin instalar bibliotecas externas:

```powershell
python actividades/analisis_texto_counter.py
```

El bloque `__main__` analiza el ejemplo del enunciado. Resultado esperado:

```text
{'caracteres_mas_comunes': [('e', 4), ('o', 3), ('l', 2)], 'total_caracteres': 32, 'total_sin_espacios': 27}
```
