"""Manipulación de una lista y cálculo de estadísticas básicas."""

# Lista inicial.
números = [10, 20, 30, 40, 50]

# Añadir 60 al final e insertar 15 entre 10 y 20.
números.append(60)
números.insert(1, 15)

# Eliminar el valor 30.
números.remove(30)

# Calcular la suma y el promedio de la lista resultante.
suma = sum(números)
promedio = suma / len(números)

print("Lista resultante:", números)
print("Suma:", suma)
print("Promedio:", promedio)
