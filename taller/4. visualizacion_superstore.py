"""Trabajo 4: visualización de ventas con Matplotlib y Seaborn.

Ejecutar: python "4. visualizacion_superstore.py"
Los resultados se guardan en resultados_trabajo4, junto a este archivo.
"""

from pathlib import Path

import matplotlib

# Permite guardar los gráficos incluso sin una interfaz gráfica disponible.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd
import seaborn as sns


RAIZ = Path(__file__).resolve().parent
RUTA_DATOS = RAIZ / "superstore_dataset2012.csv"
if not RUTA_DATOS.is_file():
    RUTA_DATOS = RAIZ / "4.superstore_dataset2012.csv"
CARPETA_RESULTADOS = RAIZ / "resultados_trabajo4"
NUMERICAS = ["Sales", "Profit", "Quantity", "Discount", "Shipping Cost"]


def cargar_y_preparar_datos(ruta):
    """Explora el CSV y limpia únicamente las columnas necesarias."""
    try:
        datos = pd.read_csv(ruta, encoding="utf-8-sig")
    except UnicodeDecodeError:
        datos = pd.read_csv(ruta, encoding="cp1252")

    requeridas = NUMERICAS + ["Order Date", "Ship Date", "Category", "Segment"]
    faltantes = set(requeridas) - set(datos.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {sorted(faltantes)}")

    print(f"Dimensiones originales: {datos.shape}")
    print("\nPrimeros registros:")
    print(datos.head().to_string(index=False))
    print("\nTipos originales:")
    print(datos.dtypes.to_string())
    print("\nValores nulos por columna:")
    print(datos.isna().sum().to_string())

    originales = len(datos)
    for columna in NUMERICAS:
        datos[columna] = pd.to_numeric(datos[columna], errors="coerce")
    datos[NUMERICAS] = datos[NUMERICAS].replace([np.inf, -np.inf], np.nan)
    # El archivo usa día/mes/año: 1/2/2012 corresponde al 1 de febrero.
    for columna in ["Order Date", "Ship Date"]:
        # Hay fechas con barras y con guiones, por ejemplo 13-01-2012.
        fechas = datos[columna].astype("string").str.replace("-", "/", regex=False)
        datos[columna] = pd.to_datetime(fechas, format="%d/%m/%Y", errors="coerce")
    for columna in ["Category", "Segment"]:
        datos[columna] = datos[columna].astype("string").str.strip().replace("", pd.NA)

    # No descartamos ventas por códigos postales ausentes. No imputamos valores
    # financieros ni eliminamos beneficios negativos: representan pérdidas.
    datos = datos.dropna(subset=requeridas).copy()
    validas = (
        (datos["Sales"] >= 0)
        & (datos["Quantity"] > 0)
        & (datos["Quantity"] % 1 == 0)
        & datos["Discount"].between(0, 1)
        & (datos["Shipping Cost"] >= 0)
        & (datos["Ship Date"] >= datos["Order Date"])
    )
    datos = datos.loc[validas].copy()
    if datos.empty:
        raise ValueError("No hay registros válidos para generar las visualizaciones.")
    datos["Quantity"] = datos["Quantity"].astype(int)
    print(f"\nFilas válidas: {len(datos)}; filas descartadas: {originales - len(datos)}")
    print("\nTipos después de la preparación:")
    print(datos[requeridas].dtypes.to_string())
    print("\nResumen numérico:")
    print(datos[NUMERICAS].describe().round(2).to_string())
    return datos


def crear_visualizaciones(datos):
    """Crea seis gráficos complementarios en un panel de subplots."""
    sns.set_theme(style="whitegrid", context="notebook")
    categorias = sorted(datos["Category"].unique())
    segmentos = sorted(datos["Segment"].unique())
    colores = dict(zip(categorias, sns.color_palette("colorblind", len(categorias))))
    fig, ejes = plt.subplots(2, 3, figsize=(20, 12), layout="constrained")
    fig.suptitle("Superstore: ventas, beneficios y comportamiento comercial", fontsize=20)

    # 1. Univariante Matplotlib: la cola derecha y la diferencia media/mediana
    # permiten detectar que pocas ventas grandes elevan el promedio.
    ax = ejes[0, 0]
    ax.hist(datos["Sales"], bins=45, color="#3478a5", edgecolor="white")
    ax.axvline(datos["Sales"].median(), color="#b94a00", linestyle="--",
               label=f"Mediana: {datos['Sales'].median():,.2f}")
    ax.set(title="1. Distribución de ventas (Matplotlib)", xlabel="Ventas por registro", ylabel="Número de registros")
    ax.legend()

    # 2. Univariante Seaborn: el boxplot muestra dispersión, mediana y valores
    # extremos. Se conservan pérdidas y observaciones atípicas reales.
    ax = ejes[0, 1]
    sns.boxplot(data=datos, x="Category", y="Profit", hue="Category", order=categorias,
                palette=colores, legend=False, fliersize=2, ax=ax)
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set(title="2. Beneficios por categoría (Seaborn)", xlabel="Categoría", ylabel="Beneficio por registro")

    # 3. Bivariante Matplotlib: los puntos bajo cero identifican ventas con
    # pérdidas; una venta alta no garantiza un beneficio alto.
    ax = ejes[0, 2]
    for categoria in categorias:
        grupo = datos.loc[datos["Category"] == categoria]
        ax.scatter(grupo["Sales"], grupo["Profit"], s=12, alpha=0.4,
                   color=colores[categoria], label=categoria, rasterized=True)
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set(title="3. Ventas frente a beneficios (Matplotlib)", xlabel="Ventas por registro", ylabel="Beneficio por registro")
    ax.legend(title="Categoría", fontsize=8)

    # 4. Bivariante temporal Matplotlib: se agregan todas las ventas de cada
    # mes observado. Un pico describe este período, no demuestra estacionalidad.
    ax = ejes[1, 0]
    mensuales = datos.set_index("Order Date")["Sales"].resample("MS").sum(min_count=1)
    ax.plot(mensuales.index, mensuales.values, marker="o", color="#39744a")
    ax.set(title="4. Ventas mensuales (Matplotlib)", xlabel="Mes del pedido", ylabel="Ventas totales del mes")
    ax.set_xticks(mensuales.index)
    ax.set_xticklabels(mensuales.index.strftime("%Y-%m"), rotation=45, ha="right")
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    # 5. Bivariante Seaborn: las sumas por categoría y segmento comparan
    # volumen monetario, no rentabilidad ni gasto medio por cliente.
    ax = ejes[1, 1]
    agrupadas = datos.groupby(["Category", "Segment"], as_index=False)["Sales"].sum()
    sns.barplot(data=agrupadas, x="Category", y="Sales", hue="Segment",
                order=categorias, hue_order=segmentos, palette="colorblind", errorbar=None, ax=ax)
    ax.set(title="5. Ventas por categoría y segmento (Seaborn)", xlabel="Categoría", ylabel="Ventas totales")
    ax.legend(title="Segmento", fontsize=8)
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

    # 6. Multivariante Seaborn: las correlaciones de Pearson resumen relaciones
    # lineales. No demuestran causalidad y pueden depender de valores extremos.
    ax = ejes[1, 2]
    correlaciones = datos[NUMERICAS].corr()
    etiquetas = ["Ventas", "Beneficio", "Cantidad", "Descuento", "Coste de envío"]
    sns.heatmap(correlaciones, annot=True, fmt=".2f", cmap="vlag", center=0,
                vmin=-1, vmax=1, square=True, xticklabels=etiquetas, yticklabels=etiquetas,
                cbar_kws={"label": "Correlación de Pearson", "shrink": 0.8}, ax=ax)
    ax.set_title("6. Relaciones entre variables (Seaborn)")
    ax.tick_params(axis="x", rotation=45)
    ax.tick_params(axis="y", rotation=0)

    CARPETA_RESULTADOS.mkdir(exist_ok=True)
    ruta_panel = CARPETA_RESULTADOS / "panel_superstore.png"
    fig.savefig(ruta_panel, dpi=160, bbox_inches="tight")
    # También se guarda el heatmap en una imagen independiente para facilitar
    # la lectura y su inclusión en una entrega académica.
    fig_correlacion, ax_correlacion = plt.subplots(figsize=(9, 7), layout="constrained")
    sns.heatmap(correlaciones, annot=True, fmt=".2f", cmap="vlag", center=0,
                vmin=-1, vmax=1, square=True, xticklabels=etiquetas, yticklabels=etiquetas,
                cbar_kws={"label": "Correlación de Pearson"}, ax=ax_correlacion)
    ax_correlacion.set_title("Superstore: correlaciones entre variables numéricas")
    ax_correlacion.tick_params(axis="x", rotation=45)
    fig_correlacion.savefig(CARPETA_RESULTADOS / "correlaciones_superstore.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    plt.close(fig_correlacion)
    # 7. Multivariante con Matplotlib: representa las mismas asociaciones
    # mediante imshow, sin utilizar Seaborn para construir este gráfico.
    # Los colores indican fuerza y signo; no demuestran causalidad.
    fig_mpl, ax_mpl = plt.subplots(figsize=(9, 7), layout="constrained")
    imagen = ax_mpl.imshow(correlaciones.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
    posiciones = np.arange(len(etiquetas))
    ax_mpl.set_xticks(posiciones)
    ax_mpl.set_yticks(posiciones)
    ax_mpl.set_xticklabels(etiquetas, rotation=45, ha="right")
    ax_mpl.set_yticklabels(etiquetas)
    ax_mpl.set_title("Correlaciones entre variables (Matplotlib)")
    ax_mpl.grid(False)
    for fila in posiciones:
        for columna in posiciones:
            valor = correlaciones.iloc[fila, columna]
            ax_mpl.text(columna, fila, f"{valor:.2f}", ha="center", va="center",
                        color="white" if abs(valor) > 0.5 else "black")
    fig_mpl.colorbar(imagen, ax=ax_mpl, label="Correlación de Pearson")
    fig_mpl.savefig(CARPETA_RESULTADOS / "correlaciones_matplotlib.png", dpi=160, bbox_inches="tight")
    plt.close(fig_mpl)
    return mensuales, agrupadas, correlaciones, ruta_panel


def documentar_conclusiones(datos, mensuales, agrupadas, correlaciones):
    """Guarda conclusiones calculadas a partir del CSV, sin cifras inventadas."""
    perdidas = (datos["Profit"] < 0).sum()
    medianas = datos.groupby("Category")["Profit"].median()
    mayor_grupo = agrupadas.loc[agrupadas["Sales"].idxmax()]
    texto = f"""TRABAJO 4: CONCLUSIONES DE LAS VISUALIZACIONES

Registros válidos analizados: {len(datos)}.
Período observado: {datos['Order Date'].min():%d/%m/%Y} a {datos['Order Date'].max():%d/%m/%Y}.
Ventas totales: {datos['Sales'].sum():,.2f}. Beneficio total: {datos['Profit'].sum():,.2f}.
El CSV no especifica la moneda. Cada fila es un registro de venta, no necesariamente un pedido completo.

1. Histograma: media de ventas {datos['Sales'].mean():,.2f} y mediana {datos['Sales'].median():,.2f}.
La media superior a la mediana muestra asimetría hacia ventas grandes; la mayoría de registros tiene importes menores.

2. Boxplot: medianas de beneficio por categoría:
{medianas.round(2).to_string()}
Las cajas y los puntos permiten comparar dispersión y extremos. Los valores negativos se conservan porque son pérdidas.

3. Dispersión: {perdidas} registros ({perdidas / len(datos):.2%}) tienen pérdidas.
La relación ventas-beneficios tiene correlación {correlaciones.loc['Sales', 'Profit']:.3f}; se observan ventas con beneficio negativo.
Conviene revisar precios, descuentos y costes en esos registros; el gráfico no establece causas.

4. Línea mensual: el mayor total observado corresponde a {mensuales.idxmax():%Y-%m}, con {mensuales.max():,.2f} en ventas.
Los extremos del período pueden representar meses incompletos. Este histórico no demuestra un patrón estacional repetido.

5. Barras agrupadas: la combinación con más ventas es {mayor_grupo['Category']} / {mayor_grupo['Segment']}, con {mayor_grupo['Sales']:,.2f}.
Los totales ayudan a identificar dónde se concentra el volumen comercial; no indican gasto medio por cliente.

6. Heatmap: correlación descuento-beneficio {correlaciones.loc['Discount', 'Profit']:.3f} y ventas-coste de envío {correlaciones.loc['Sales', 'Shipping Cost']:.3f}.
Las relaciones son descriptivas y lineales, sensibles a extremos; correlación no implica causalidad.

Preparación: conversión numérica y de fechas día/mes/año, validación de rangos y eliminación de nulos solo en columnas del análisis.
Los códigos postales ausentes no provocan la pérdida de filas. Los datos originales no se modifican.
"""
    (CARPETA_RESULTADOS / "conclusiones.txt").write_text(texto, encoding="utf-8")
    print("\n" + texto)


def main():
    datos = cargar_y_preparar_datos(RUTA_DATOS)
    mensuales, agrupadas, correlaciones, ruta_panel = crear_visualizaciones(datos)
    documentar_conclusiones(datos, mensuales, agrupadas, correlaciones)
    print(f"Panel guardado en: {ruta_panel}")


if __name__ == "__main__":
    main()
