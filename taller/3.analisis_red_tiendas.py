"""Trabajo 3: análisis de RetailNow con Pandas y NumPy.

Ejecutar: python 3.analisis_red_tiendas.py
Dependencias: python -m pip install -r 3.requirements.txt
"""

def display(*objetos):
    """Muestra tablas y resultados en la consola."""
    for objeto in objetos:
        if hasattr(objeto, "to_string"):
            print(objeto.to_string(index=True))
        else:
            print(objeto)
        print()

# # Trabajo 3: Análisis de datos con NumPy y Pandas
# 
# Analizamos las ventas, los inventarios y la satisfacción de clientes de RetailNow usando los tres CSV originales de `3. python_intermedio`.
# 
# **Ejecución:** abre este notebook en Visual Studio Code con las extensiones Python y Jupyter, selecciona un entorno con `pandas`, `numpy` e `ipykernel` y ejecuta las celdas en orden. Puedes instalar las dependencias con `python -m pip install -r 3.requirements.txt` desde esta carpeta.
# 
# Los datos se conservan en memoria: no se modifican los CSV. Las rutas se construyen como absolutas desde la ubicación del script; los CSV pueden estar en la carpeta de datos o junto al archivo.

from pathlib import Path
import pandas as pd
import numpy as np

CARPETA_DATOS = Path(__file__).resolve().parent / "3. python_intermedio"
if not CARPETA_DATOS.is_dir():
    CARPETA_DATOS = Path(__file__).resolve().parent
RUTA_VENTAS = CARPETA_DATOS / "sales.csv"
RUTA_INVENTARIOS = CARPETA_DATOS / "inventories.csv"
RUTA_SATISFACCION = CARPETA_DATOS / "satisfaction.csv"

for ruta in (RUTA_VENTAS, RUTA_INVENTARIOS, RUTA_SATISFACCION):
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encuentra el CSV: {ruta}")

ventas = pd.read_csv(RUTA_VENTAS)
inventarios = pd.read_csv(RUTA_INVENTARIOS)
satisfaccion = pd.read_csv(RUTA_SATISFACCION)
display(ventas.head(), inventarios.head(), satisfaccion.head())

# ## 1. Limpieza y comprobación de estructura
# 
# Verificamos las columnas requeridas, convertimos los campos numéricos y las fechas y usamos `dropna()` para eliminar filas incompletas o con conversiones inválidas. Se informa cuántas filas se eliminan. Además, rechazamos números no finitos, cantidades negativas o no enteras y satisfacción fuera de 0 a 100.
# 
# Cada fila de inventario representa el stock de un producto en una tienda. Si hay varias observaciones para el mismo par, usamos la más reciente para evitar sumar snapshots de stock. La rotación será una aproximación: relaciona las ventas de todo el período disponible con este stock, no con un inventario promedio del período.

def limpiar_datos(df, nombre, columnas_numericas, columna_fecha, columnas_texto=()):
    requeridas = set(columnas_numericas) | {columna_fecha} | set(columnas_texto)
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"{nombre}: faltan columnas {sorted(faltantes)}")
    limpio = df.copy()
    for columna in columnas_texto:
        limpio[columna] = limpio[columna].astype("string").str.strip().replace("", pd.NA)
    for columna in columnas_numericas:
        limpio[columna] = pd.to_numeric(limpio[columna], errors="coerce")
    limpio[columna_fecha] = pd.to_datetime(limpio[columna_fecha], errors="coerce")
    limpio = limpio.dropna().copy()
    print(f"{nombre}: {len(df)} filas iniciales; {len(df) - len(limpio)} eliminadas; {len(limpio)} válidas.")
    if not np.isfinite(limpio[list(columnas_numericas)].to_numpy(dtype=float)).all():
        raise ValueError(f"{nombre}: hay valores numéricos no finitos.")
    return limpio

ventas = limpiar_datos(ventas, "Ventas", ["ID_Tienda", "Cantidad_Vendida", "Precio_Unitario"], "Fecha_Venta", ["Producto"])
inventarios = limpiar_datos(inventarios, "Inventarios", ["ID_Tienda", "Stock_Disponible"], "Fecha_Actualización", ["Producto"])
satisfaccion = limpiar_datos(satisfaccion, "Satisfacción", ["ID_Tienda", "Satisfacción_Promedio"], "Fecha_Evaluación")

for df, columnas in [(ventas, ["Cantidad_Vendida", "Precio_Unitario"]), (inventarios, ["Stock_Disponible"])]:
    if (df[columnas] < 0).any().any():
        raise ValueError("Las cantidades, el stock y los precios deben ser no negativos.")
for df, columnas in [(ventas, ["ID_Tienda", "Cantidad_Vendida"]), (inventarios, ["ID_Tienda", "Stock_Disponible"]), (satisfaccion, ["ID_Tienda"])]:
    for columna in columnas:
        if (df[columna] % 1 != 0).any():
            raise ValueError(f"{columna} debe contener números enteros.")
        df[columna] = df[columna].astype(int)
if not satisfaccion["Satisfacción_Promedio"].between(0, 100).all():
    raise ValueError("La satisfacción debe estar entre 0 y 100.")
if ventas.empty or inventarios.empty or satisfaccion.empty:
    raise ValueError("Se necesitan datos válidos en los tres archivos para completar el análisis.")

inventarios = (inventarios.sort_values("Fecha_Actualización")
              .drop_duplicates(["ID_Tienda", "Producto"], keep="last").copy())
display(pd.DataFrame({"Ventas": ventas.dtypes.astype(str), "Inventarios": inventarios.dtypes.astype(str), "Satisfacción": satisfaccion.dtypes.astype(str)}))

# ## 2. Exploración de ventas
# 
# `Total_Ventas` representa ingresos monetarios por registro: cantidad vendida × precio unitario. Distinguimos estos ingresos de las unidades vendidas. Agrupamos por producto, por tienda y por ambos campos, y obtenemos estadísticas con `describe()`; el percentil 50 % corresponde a la mediana.

ventas["Total_Ventas"] = ventas["Cantidad_Vendida"] * ventas["Precio_Unitario"]
ventas_por_producto = ventas.groupby("Producto", as_index=False).agg(
    Unidades_Vendidas=("Cantidad_Vendida", "sum"), Ingresos_Totales=("Total_Ventas", "sum"))
ventas_por_tienda = ventas.groupby("ID_Tienda", as_index=False).agg(
    Unidades_Vendidas=("Cantidad_Vendida", "sum"), Ingresos_Totales=("Total_Ventas", "sum"))
ventas_por_tienda_producto = ventas.groupby(["ID_Tienda", "Producto"], as_index=False).agg(
    Unidades_Vendidas=("Cantidad_Vendida", "sum"), Ingresos_Totales=("Total_Ventas", "sum"))
print("Ventas por producto, por tienda y por tienda/producto:")
display(ventas_por_producto, ventas_por_tienda, ventas_por_tienda_producto)
print("Resumen estadístico de los registros de ventas:")
display(ventas[["Cantidad_Vendida", "Precio_Unitario", "Total_Ventas"]].describe())

if "Categoria" in ventas.columns or "Categoría" in ventas.columns:
    categoria = "Categoria" if "Categoria" in ventas.columns else "Categoría"
    display(ventas.groupby(["ID_Tienda", categoria]).agg(
        Promedio_Unidades=("Cantidad_Vendida", "mean"), Promedio_Ingresos=("Total_Ventas", "mean")))
else:
    print("Los CSV no incluyen categorías: no se inventan clasificaciones de productos.")

# ## 3. Rotación de inventarios
# 
# Unimos las unidades vendidas con el stock usando **tienda y producto**, para no mezclar productos de distintas tiendas. La columna `Rotacion_Inventario` se calcula como unidades vendidas / stock disponible. Para cada tienda calculamos la misma proporción sobre las sumas; no promediamos las proporciones de los productos.
# 
# Aplicamos literalmente el criterio solicitado: **rotación < 0.10**, equivalente a ventas inferiores al 10 % del stock. Este criterio indica baja salida o posible exceso de stock; por sí solo no indica falta de existencias. Si el stock es cero, la proporción queda indefinida (`NaN`) y se muestra por separado. También se informa de ventas sin una correspondencia en inventario.

unidades_por_producto = ventas_por_tienda_producto[["ID_Tienda", "Producto", "Unidades_Vendidas"]]
inventarios = inventarios.merge(unidades_por_producto, on=["ID_Tienda", "Producto"], how="left", validate="one_to_one")
inventarios["Unidades_Vendidas"] = inventarios["Unidades_Vendidas"].fillna(0).astype(int)
inventarios["Rotacion_Inventario"] = inventarios["Unidades_Vendidas"] / inventarios["Stock_Disponible"].replace(0, np.nan)
inventarios["Porcentaje_Vendido"] = inventarios["Rotacion_Inventario"] * 100

rotacion_por_tienda = inventarios.groupby("ID_Tienda", as_index=False).agg(
    Unidades_Vendidas=("Unidades_Vendidas", "sum"), Stock_Disponible=("Stock_Disponible", "sum"))
rotacion_por_tienda["Rotacion_Inventario"] = rotacion_por_tienda["Unidades_Vendidas"] / rotacion_por_tienda["Stock_Disponible"].replace(0, np.nan)
rotacion_por_tienda["Porcentaje_Vendido"] = rotacion_por_tienda["Rotacion_Inventario"] * 100
productos_criticos = inventarios.loc[inventarios["Rotacion_Inventario"] < 0.10]
tiendas_criticas = rotacion_por_tienda.loc[rotacion_por_tienda["Rotacion_Inventario"] < 0.10]
ventas_sin_stock = unidades_por_producto.merge(inventarios[["ID_Tienda", "Producto"]], on=["ID_Tienda", "Producto"], how="left", indicator=True)
ventas_sin_stock = ventas_sin_stock.loc[ventas_sin_stock["_merge"] == "left_only"]

print("Inventario con rotación por producto y resumen por tienda:")
display(inventarios, rotacion_por_tienda)
print("Productos y tiendas con rotación inferior al 10 %:")
display(productos_criticos, tiendas_criticas)
if tiendas_criticas.empty:
    print("Ninguna tienda cumple el criterio de inventario crítico del ejercicio.")
print("Productos sin stock disponible y ventas sin registro de stock:")
display(inventarios.loc[inventarios["Stock_Disponible"] == 0], ventas_sin_stock)

# ## 4. Satisfacción del cliente y ventas
# 
# Calculamos la satisfacción media de cada tienda y la relacionamos con sus unidades e ingresos. Si hubiera varias evaluaciones, esta sería una media simple por registro, porque no se proporcionan cantidades de encuestados para ponderarla. Filtramos satisfacción estrictamente menor al 60 %.
# 
# La correlación es descriptiva: cinco tiendas son una muestra pequeña y una asociación no demuestra que la satisfacción cause cambios en las ventas.

satisfaccion_por_tienda = satisfaccion.groupby("ID_Tienda", as_index=False).agg(
    Satisfaccion_Promedio=("Satisfacción_Promedio", "mean"))
rendimiento = ventas_por_tienda.merge(satisfaccion_por_tienda, on="ID_Tienda", how="outer", validate="one_to_one")
tiendas_baja_satisfaccion = rendimiento.loc[rendimiento["Satisfaccion_Promedio"] < 60]
display(rendimiento, tiendas_baja_satisfaccion)
correlacion = rendimiento["Ingresos_Totales"].corr(rendimiento["Satisfaccion_Promedio"])
print(f"Correlación de Pearson entre ingresos y satisfacción: {correlacion:.4f}")
for _, tienda in tiendas_baja_satisfaccion.iterrows():
    print(f"Tienda {int(tienda['ID_Tienda'])}: satisfacción {tienda['Satisfaccion_Promedio']:.1f} %.")
    print("Recomendaciones: revisar quejas y tiempos de atención; capacitar al personal; comprobar disponibilidad y calidad de productos; repetir la encuesta para medir mejoras.")
if tiendas_baja_satisfaccion.empty:
    print("No hay tiendas con satisfacción inferior al 60 %.")

# ## 5. Estadísticas con NumPy
# 
# Convertimos explícitamente `Total_Ventas` a un array con `.to_numpy()`. Calculamos mediana y desviación estándar de los ingresos **por registro de venta**. Usamos `ddof=0` para describir la población de registros disponible; `describe()` de Pandas usa la desviación muestral (`ddof=1`), por lo que sus resultados pueden diferir.

array_ventas = ventas["Total_Ventas"].to_numpy(dtype=float)
mediana_ventas = np.median(array_ventas)
desviacion_ventas = np.std(array_ventas, ddof=0)
print(f"Mediana de Total_Ventas por registro: {mediana_ventas:.2f}")
print(f"Desviación estándar poblacional: {desviacion_ventas:.2f}")

# ## 6. Simulación reproducible de ventas futuras
# 
# Simulamos 1 000 escenarios de ingresos para cada tienda en un período de igual duración al observado. Suponemos un cambio relativo normal con media del 5 % y desviación del 10 %. Son supuestos ilustrativos, no estimaciones aprendidas de los datos ni un pronóstico validado.
# 
# Usamos `np.random.default_rng(42)` para fijar la semilla. Limitamos los factores a cero como mínimo para evitar ingresos negativos y resumimos cada tienda con media, mediana, desviación y percentiles 5 y 95. Estos percentiles describen los escenarios simulados, no un intervalo de confianza estadístico.

SEMILLA = 42
NUM_ESCENARIOS = 1000
rng = np.random.default_rng(SEMILLA)
ingresos_base = ventas_por_tienda["Ingresos_Totales"].to_numpy(dtype=float)
cambios = rng.normal(loc=0.05, scale=0.10, size=(NUM_ESCENARIOS, len(ingresos_base)))
proyecciones = ingresos_base[np.newaxis, :] * np.maximum(1 + cambios, 0)
resumen_proyecciones = pd.DataFrame({
    "ID_Tienda": ventas_por_tienda["ID_Tienda"].to_numpy(),
    "Ingresos_Base": ingresos_base,
    "Media_Proyectada": np.mean(proyecciones, axis=0),
    "Mediana_Proyectada": np.median(proyecciones, axis=0),
    "Desviacion_Proyectada": np.std(proyecciones, axis=0),
    "Percentil_5": np.percentile(proyecciones, 5, axis=0),
    "Percentil_95": np.percentile(proyecciones, 95, axis=0),
})
display(resumen_proyecciones.round(2))
totales_simulados = np.sum(proyecciones, axis=1)
print(f"Ingreso total observado: {np.sum(ingresos_base):.2f}")
print(f"Media del ingreso total simulado: {np.mean(totales_simulados):.2f}")
print(f"Mediana del ingreso total simulado: {np.median(totales_simulados):.2f}")
print(f"Desviación del ingreso total simulado: {np.std(totales_simulados):.2f}")

# ## 7. Conclusiones
# 
# Los CSV originales contienen 10 registros de ventas, 10 de inventarios y 5 evaluaciones de satisfacción; no se eliminan filas por nulos.
# 
# - Se vendieron **250 unidades** y se obtuvieron **50 500** en ingresos (los archivos no indican la moneda).
# - Las tiendas **4 y 5** comparten los mayores ingresos (**13 000** cada una). La tienda **4** tiene las mayores unidades vendidas (**60**). La tienda **1** tiene los menores ingresos (**5 000**) y unidades (**35**).
# - Ningún producto ni tienda tiene una proporción vendida inferior al **10 %**. Las proporciones por tienda van del **38.89 %** al **52.38 %**.
# - La tienda **5** tiene satisfacción del **55 %**, inferior al umbral, aunque alcanza **13 000** en ingresos. Conviene investigar sus quejas y dar seguimiento a las mejoras del servicio.
# - La mediana de ingresos por registro es **3 500** y la desviación estándar poblacional es aproximadamente **3 189.44**.
# - Las simulaciones permiten explorar un supuesto de crecimiento, pero no sustituyen un pronóstico con histórico suficiente.
# 
# Para tomar decisiones de reposición se necesitarían también inventarios medios, fechas comparables, plazos de entrega y demanda histórica. Las recomendaciones son hipótesis de mejora, no efectos causales demostrados.
