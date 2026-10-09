"""Encontrar elementos comunes y únicos entre dos listas con conjuntos."""

lista1 = [1, 2, 3, 4, 5, 6]
lista2 = [4, 5, 6, 7, 8, 9]

conjunto1 = set(lista1)
conjunto2 = set(lista2)

interseccion = conjunto1 & conjunto2
solo_primera = conjunto1 - conjunto2
solo_segunda = conjunto2 - conjunto1
union = conjunto1 | conjunto2

# Ordenar solo para mostrar resultados en un orden predecible.
print("Intersección:", sorted(interseccion))
print("Solo en la primera lista:", sorted(solo_primera))
print("Solo en la segunda lista:", sorted(solo_segunda))
print("Unión:", sorted(union))
