"""Creación y desempaquetado de una tupla con datos de contacto."""

contacto = ("Ana García", "ana@ejemplo.com", "555-1234")

# Desempaquetar los tres elementos en variables independientes.
nombre, email, telefono = contacto

print(nombre)
print(email)
print(telefono)

# La concatenación crea otra tupla y conserva la original.
# La coma indica que ("Madrid",) es una tupla de un solo elemento.
contacto_completo = contacto + ("Madrid",)
print("Contacto completo:", contacto_completo)
