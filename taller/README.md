# Talleres de Python

Los cuatro trabajos están organizados en esta carpeta. Ejecuta los comandos desde `taller`; usa comillas cuando el nombre contenga espacios.

| Trabajo | Archivo principal | Documentación |
| --- | --- | --- |
| 1. Sintaxis y programación estructurada | `1. calculadora_promedios.py` | [README del Trabajo 1](1.README.md) |
| 2. Programación orientada a objetos | `2. sistema_inventario.py` | [README del Trabajo 2](2.README.md) |
| 3. Análisis con Pandas y NumPy | `3.analisis_red_tiendas.ipynb` y versión `.py` | [README del Trabajo 3](3.README.md) |
| 4. Visualización | `4. visualizacion_superstore.py` | [README del Trabajo 4](<4. README.md>) |

## Instalación y ejecución

```powershell
python -m pip install -r 3.requirements.txt -r "4. requirements.txt"
python "1. calculadora_promedios.py"
python "2. sistema_inventario.py"
python 3.analisis_red_tiendas.py
python "4. visualizacion_superstore.py"
```

Cada programa es independiente; ejecuta el que corresponda. Los trabajos 1 y 2 no requieren dependencias externas. Para el Trabajo 3 en notebook, selecciona el entorno instalado como kernel de Jupyter y ejecuta todas las celdas.

## Datos y resultados

El Trabajo 3 utiliza los CSV de `3. python_intermedio`. Se recuperaron sus registros originales mostrados anteriormente en el proyecto. El Trabajo 4 utiliza `4.superstore_dataset2012.csv`, recuperado desde el enlace original del enunciado. Ningún análisis modifica sus CSV.

Las figuras y conclusiones del Trabajo 4 se guardan en `resultados_trabajo4`. El notebook del Trabajo 3 contiene resultados guardados. Los prefijos numéricos organizan los archivos; para subirlos a la plataforma puedes usar los nombres del enunciado, indicados en cada README.

## Validación reproducible

```powershell
python validar_taller.py
```

Este comando comprueba los cuatro trabajos, ejecuta el análisis y las visualizaciones, actualiza los resultados guardados del notebook y escribe `VALIDACION.txt`. Si una comprobación falla, termina con el error en lugar de marcarla como correcta. Los README de cada trabajo relacionan los puntos del enunciado con su implementación.
