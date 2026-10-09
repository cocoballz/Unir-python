"""Sistema básico de inventario con programación orientada a objetos."""

from math import isfinite


class Producto:
    """Representa un producto con nombre, precio y cantidad disponibles."""

    def __init__(self, nombre: str, precio: float, cantidad: int):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        if not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")

        self.nombre = nombre.strip()
        self.actualizar_precio(precio)
        self.actualizar_cantidad(cantidad)

    def actualizar_precio(self, nuevo_precio):
        """Valida y actualiza el precio sin modificarlo si el dato es inválido."""
        if isinstance(nuevo_precio, bool) or not isinstance(nuevo_precio, (int, float)):
            raise TypeError("El precio debe ser un número.")
        if not isfinite(nuevo_precio) or nuevo_precio < 0:
            raise ValueError("El precio debe ser finito y mayor o igual que cero.")
        self.precio = float(nuevo_precio)

    def actualizar_cantidad(self, nueva_cantidad):
        """Valida y actualiza la cantidad de unidades del producto."""
        if isinstance(nueva_cantidad, bool) or not isinstance(nueva_cantidad, int):
            raise TypeError("La cantidad debe ser un número entero.")
        if nueva_cantidad < 0:
            raise ValueError("La cantidad debe ser mayor o igual que cero.")
        self.cantidad = nueva_cantidad

    def calcular_valor_total(self):
        """Devuelve el precio multiplicado por la cantidad."""
        return self.precio * self.cantidad

    def __str__(self):
        return (
            f"{self.nombre} | Precio: {self.precio:.2f} | "
            f"Cantidad: {self.cantidad} | Valor total: {self.calcular_valor_total():.2f}"
        )


class Inventario:
    """Gestiona una lista de objetos Producto."""

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        """Añade únicamente objetos de tipo Producto."""
        if not isinstance(producto, Producto):
            raise TypeError("Solo se pueden agregar objetos de tipo Producto.")
        self.productos.append(producto)

    def buscar_producto(self, nombre):
        """Busca el nombre completo sin distinguir mayúsculas y minúsculas."""
        if not isinstance(nombre, str):
            raise TypeError("El nombre de búsqueda debe ser una cadena de texto.")
        if not nombre.strip():
            raise ValueError("Debes escribir el nombre del producto que deseas buscar.")

        for producto in self.productos:
            if producto.nombre.casefold() == nombre.strip().casefold():
                return producto
        return None

    def calcular_valor_inventario(self):
        """Suma el valor de los productos; devuelve 0.0 si no hay productos."""
        return sum((producto.calcular_valor_total() for producto in self.productos), 0.0)

    def listar_productos(self):
        """Muestra los productos o informa que el inventario está vacío."""
        if not self.productos:
            print("El inventario está vacío.")
            return

        print("\n=== Productos del inventario ===")
        for indice, producto in enumerate(self.productos, start=1):
            print(f"{indice}. {producto}")


def menu_principal(inventario):
    """Procesa las opciones del menú hasta que el usuario elige salir."""
    while True:
        print("\n=== Sistema de inventario ===")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Listar productos")
        print("4. Calcular valor total del inventario")
        print("5. Salir")

        try:
            opcion = input("Selecciona una opción: ").strip()

            if opcion == "1":
                nombre = input("Nombre del producto: ")
                try:
                    precio = float(input("Precio (usa punto para decimales): "))
                    cantidad = int(input("Cantidad de unidades: "))
                except ValueError:
                    raise ValueError("Ingresa un precio numérico y una cantidad entera.") from None

                producto = Producto(nombre, precio, cantidad)
                inventario.agregar_producto(producto)
                print(f"Producto agregado: {producto}")

            elif opcion == "2":
                nombre = input("Nombre completo del producto a buscar: ")
                producto = inventario.buscar_producto(nombre)
                if producto is None:
                    raise LookupError(f"No se encontró el producto '{nombre.strip()}'.")
                print(f"Producto encontrado: {producto}")

            elif opcion == "3":
                inventario.listar_productos()

            elif opcion == "4":
                print(f"Valor total del inventario: {inventario.calcular_valor_inventario():.2f}")

            elif opcion == "5":
                print("¡Gracias por usar el sistema de inventario! Hasta pronto.")
                break

            else:
                print("Opción inválida. Selecciona un número del 1 al 5.")

        except (ValueError, TypeError, LookupError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nEntrada finalizada. Hasta pronto.")
            break


if __name__ == "__main__":
    inventario = Inventario()
    menu_principal(inventario)
