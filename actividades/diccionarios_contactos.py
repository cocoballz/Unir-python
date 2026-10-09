"""Almacenar, consultar y modificar contactos en un diccionario."""

contactos = {
    "persona1": {"nombre": "Ana", "telefono": "123456789", "email": "ana@ejemplo.com"},
    "persona2": {"nombre": "Luis", "telefono": "234567890", "email": "luis@ejemplo.com"},
    "persona3": {"nombre": "Marta", "telefono": "345678901", "email": "marta@ejemplo.com"},
}

# Consultar el correo de la segunda persona añadida.
print("Correo de la segunda persona:", contactos["persona2"]["email"])

# Añadir un cuarto contacto.
contactos["persona4"] = {
    "nombre": "Carlos",
    "telefono": "456789012",
    "email": "carlos@ejemplo.com",
}

# Modificar el teléfono de la primera persona.
contactos["persona1"]["telefono"] = "987654321"
print("Teléfono actualizado de Ana:", contactos["persona1"]["telefono"])

# Recorrer los contactos y mostrar todos sus nombres.
print("Nombres de los contactos:")
for contacto in contactos.values():
    print(contacto["nombre"])
