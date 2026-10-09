"""Verifica los cuatro trabajos y actualiza los resultados del notebook.

Ejecutar desde taller: python validar_taller.py
Requiere las dependencias de los trabajos 3 y 4.
"""

import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd
from PIL import Image

BASE = Path(__file__).resolve().parent
resultados = []


def esperar_error(tipo, funcion, *argumentos):
    try:
        funcion(*argumentos)
    except tipo:
        return
    raise AssertionError(f"Se esperaba {tipo.__name__}")


def ejecutar_menu(funcion, entradas, *argumentos):
    salida = io.StringIO()
    with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(salida):
        funcion(*argumentos)
    return salida.getvalue()


def validar_1():
    modulo = runpy.run_path(str(BASE / "1. calculadora_promedios.py"))
    assert modulo["calcular_promedio"]([0, 5, 10]) == 5
    assert modulo["calcular_promedio"]([]) == 0.0
    assert modulo["determinar_estado"]([0, 5, 10]) == ([1, 2], [0])
    assert modulo["determinar_estado"]([5, 7], 6) == ([1], [0])
    assert modulo["encontrar_extremos"]([8, 2, 8]) == (0, 1)
    assert modulo["encontrar_extremos"]([4]) == (0, 0)
    assert modulo["encontrar_extremos"]([]) == (None, None)
    entradas = [" Matemáticas ", "abc", "-1", "11", "nan", "inf", "10", "quizá", "s", "Historia", "4", "n"]
    with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(io.StringIO()):
        assert modulo["ingresar_calificaciones"]() == (["Matemáticas", "Historia"], [10.0, 4.0])
    for entradas, esperado in [([""], "No se ingresó ninguna materia"),
                              (["A", "10", "s", "B", "4", "n"], "Promedio general: 7.00"),
                              (["A", "5", "n"], "Materias reprobadas:\nNinguna"),
                              (["A", "0", "n"], "Materias aprobadas:\nNinguna")]:
        salida = ejecutar_menu(modulo["main"], entradas)
        assert esperado in salida and "Hasta pronto" in salida
    resultados.append("Trabajo 1: funciones, listas, límites, errores, empates, vacío y resumen: OK.")


def validar_2():
    modulo = runpy.run_path(str(BASE / "2. sistema_inventario.py"))
    Producto, Inventario = modulo["Producto"], modulo["Inventario"]
    producto = Producto(" Cuaderno ", 2.5, 4)
    assert producto.nombre == "Cuaderno" and producto.calcular_valor_total() == 10
    producto.actualizar_precio(3)
    producto.actualizar_cantidad(5)
    assert producto.calcular_valor_total() == 15 and "15.00" in str(producto)
    for argumentos, error in [(("", 1, 1), ValueError), ((1, 1, 1), TypeError),
                              (("A", -1, 1), ValueError), (("A", "2", 1), TypeError),
                              (("A", np.nan, 1), ValueError), (("A", np.inf, 1), ValueError),
                              (("A", 1, -1), ValueError), (("A", 1, 1.5), TypeError),
                              (("A", True, 1), TypeError), (("A", 1, True), TypeError)]:
        esperar_error(error, Producto, *argumentos)
    esperar_error(ValueError, producto.actualizar_precio, -1)
    esperar_error(ValueError, producto.actualizar_cantidad, -1)
    assert producto.precio == 3 and producto.cantidad == 5
    inventario = Inventario()
    assert inventario.calcular_valor_inventario() == 0
    inventario.agregar_producto(producto)
    inventario.agregar_producto(Producto("Lápiz", 1, 2))
    assert inventario.calcular_valor_inventario() == 17
    assert inventario.buscar_producto("CUADERNO") is producto
    assert inventario.buscar_producto("Cuad") is None
    esperar_error(TypeError, inventario.agregar_producto, "A")
    esperar_error(ValueError, inventario.buscar_producto, " ")
    entradas = ["3", "4", "x", "1", "A", "abc", "1", "A", "2", "-1", "1", "A", "2.5", "4", "2", "a", "2", "B", "3", "4", "5"]
    salida = ejecutar_menu(modulo["menu_principal"], entradas, Inventario())
    for texto in ["inventario está vacío", "Opción inválida", "Error:", "Producto agregado", "Producto encontrado", "No se encontró", "Valor total del inventario: 10.00", "Hasta pronto"]:
        assert texto in salida, texto
    resultados.append("Trabajo 2: clases, actualizaciones, tipos, búsqueda, totales y cinco opciones: OK.")


def comprobar_analisis(entorno):
    assert entorno["ventas_por_tienda"]["Unidades_Vendidas"].sum() == 250
    assert entorno["ventas_por_tienda"]["Ingresos_Totales"].sum() == 50500
    assert entorno["tiendas_criticas"].empty and entorno["productos_criticos"].empty
    assert entorno["tiendas_baja_satisfaccion"]["ID_Tienda"].tolist() == [5]
    assert entorno["mediana_ventas"] == 3500
    np.testing.assert_allclose(entorno["desviacion_ventas"], 3189.4356867634124)
    np.testing.assert_allclose(entorno["rotacion_por_tienda"]["Rotacion_Inventario"], [35/90, 55/105, 50/110, 60/120, 50/100])
    assert entorno["proyecciones"].shape == (1000, 5)
    assert (entorno["proyecciones"] >= 0).all()
    np.testing.assert_array_equal(entorno["cambios"], np.random.default_rng(42).normal(0.05, 0.10, (1000, 5)))


def validar_3():
    with contextlib.redirect_stdout(io.StringIO()):
        entorno = runpy.run_path(str(BASE / "3.analisis_red_tiendas.py"))
    comprobar_analisis(entorno)
    limpiar = entorno["limpiar_datos"]
    ejemplo = pd.DataFrame({"N": [1, None, "abc"], "Fecha": ["2023-01-01"] * 3})
    with contextlib.redirect_stdout(io.StringIO()):
        assert len(limpiar(ejemplo, "Prueba", ["N"], "Fecha")) == 1
        esperar_error(ValueError, limpiar, ejemplo, "Prueba", ["Ausente"], "Fecha")
        esperar_error(ValueError, limpiar, pd.DataFrame({"N": [np.inf], "Fecha": ["2023-01-01"]}), "Prueba", ["N"], "Fecha")

    ruta = BASE / "3.analisis_red_tiendas.ipynb"
    notebook = json.loads(ruta.read_text(encoding="utf-8"))
    entorno_nb = {}
    cwd_anterior = Path.cwd()
    try:
        os.chdir(BASE)
        numero = 0
        for celda in notebook["cells"]:
            if celda["cell_type"] != "code":
                continue
            numero += 1
            fuente = celda["source"]
            if isinstance(fuente, list):
                fuente = "".join(fuente)
            salidas = []
            def mostrar(*objetos):
                for objeto in objetos:
                    contenido = {"text/plain": repr(objeto)}
                    if hasattr(objeto, "_repr_html_"):
                        contenido["text/html"] = objeto._repr_html_()
                    salidas.append({"output_type": "display_data", "metadata": {}, "data": contenido})
            entorno_nb["display"] = mostrar
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exec(compile(fuente.replace("from IPython.display import display", ""), f"celda_{numero}", "exec"), entorno_nb)
            if buffer.getvalue():
                salidas.append({"output_type": "stream", "name": "stdout", "text": buffer.getvalue()})
            celda["outputs"] = salidas
            celda["execution_count"] = numero
        comprobar_analisis(entorno_nb)
        notebook["metadata"]["language_info"]["version"] = "3.12"
        ruta.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    finally:
        os.chdir(cwd_anterior)
    resultados.append("Trabajo 3: script y siete celdas, limpieza, totales, rotación, estadísticas y semilla: OK.")


def validar_4():
    modulo = runpy.run_path(str(BASE / "4. visualizacion_superstore.py"))
    with contextlib.redirect_stdout(io.StringIO()):
        datos = modulo["cargar_y_preparar_datos"](modulo["RUTA_DATOS"])
    assert len(datos) == 4246
    np.testing.assert_allclose(datos["Sales"].sum(), 1006427.18386, rtol=1e-7)
    assert pd.api.types.is_datetime64_any_dtype(datos["Order Date"])
    assert (datos["Profit"] < 0).any()
    assert datos["Postal Code"].isna().sum() == 3423
    mensuales, agrupadas, correlaciones, ruta = modulo["crear_visualizaciones"](datos)
    with contextlib.redirect_stdout(io.StringIO()):
        modulo["documentar_conclusiones"](datos, mensuales, agrupadas, correlaciones)
    for nombre in ["panel_superstore.png", "correlaciones_superstore.png", "correlaciones_matplotlib.png"]:
        with Image.open(ruta.parent / nombre) as imagen:
            assert imagen.width > 800 and imagen.height > 600
            imagen.verify()
    with tempfile.TemporaryDirectory(dir=BASE, prefix="validacion_temporal_") as temporal:
        ruta_prueba = Path(temporal) / "prueba.csv"
        muestra = datos.head(2).copy()
        muestra["Order Date"] = ["01-02-2012", "01/02/2012"]
        muestra["Ship Date"] = ["07-02-2012", "06/02/2012"]
        muestra.to_csv(ruta_prueba, index=False)
        with contextlib.redirect_stdout(io.StringIO()):
            assert len(modulo["cargar_y_preparar_datos"](ruta_prueba)) == 2
            muestra.loc[0, "Sales"] = -1
            muestra.to_csv(ruta_prueba, index=False)
            assert len(modulo["cargar_y_preparar_datos"](ruta_prueba)) == 1
            muestra.drop(columns="Sales").to_csv(ruta_prueba, index=False)
            esperar_error(ValueError, modulo["cargar_y_preparar_datos"], ruta_prueba)
            muestra.iloc[:0].to_csv(ruta_prueba, index=False)
            esperar_error(ValueError, modulo["cargar_y_preparar_datos"], ruta_prueba)
    resultados.append("Trabajo 4: carga, fechas, limpieza, seis subplots y matrices de ambas bibliotecas: OK.")


if __name__ == "__main__":
    validar_1()
    validar_2()
    validar_3()
    validar_4()
    informe = "\n".join(resultados) + "\n"
    (BASE / "VALIDACION.txt").write_text(informe, encoding="utf-8")
    print(informe)
