"""Calculadora de promedios escolares con programación estructurada."""


def ingresar_calificaciones():
    """Solicita materias y notas, y devuelve dos listas relacionadas por índice."""
    materias = []
    calificaciones = []

    while True:
        materia = input("Nombre de la materia (Enter para terminar): ").strip()
        if not materia:
            break

        while True:
            entrada = input("Calificación entre 0 y 10: ").strip()
            try:
                calificacion = float(entrada)
            except ValueError:
                print("Entrada inválida. Debes ingresar un número.")
                continue

            if 0 <= calificacion <= 10:
                break
            print("La calificación debe estar entre 0 y 10.")

        materias.append(materia)
        calificaciones.append(calificacion)

        while True:
            continuar = input("¿Deseas ingresar otra materia? (s/n): ").strip().lower()
            if continuar in ("s", "si", "sí", "n", "no"):
                break
            print("Respuesta inválida. Escribe s o n.")

        if continuar in ("n", "no"):
            break

    return materias, calificaciones


def calcular_promedio(calificaciones):
    """Devuelve el promedio, o 0.0 si la lista está vacía."""
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)


def determinar_estado(calificaciones, umbral=5.0):
    """Devuelve los índices de las materias aprobadas y reprobadas."""
    aprobadas = []
    reprobadas = []

    for indice, calificacion in enumerate(calificaciones):
        if calificacion >= umbral:
            aprobadas.append(indice)
        else:
            reprobadas.append(indice)

    return aprobadas, reprobadas


def encontrar_extremos(calificaciones):
    """Devuelve índices de mayor y menor nota; en empates toma el primero."""
    if not calificaciones:
        return None, None

    indice_maximo = calificaciones.index(max(calificaciones))
    indice_minimo = calificaciones.index(min(calificaciones))
    return indice_maximo, indice_minimo


def main():
    """Recoge los datos y muestra el resumen escolar."""
    print("=== Calculadora de promedios escolares ===")
    materias, calificaciones = ingresar_calificaciones()

    if not materias:
        print("No se ingresó ninguna materia.")
    else:
        promedio = calcular_promedio(calificaciones)
        aprobadas, reprobadas = determinar_estado(calificaciones)
        indice_maximo, indice_minimo = encontrar_extremos(calificaciones)

        print("\n=== Resumen final ===")
        for indice, materia in enumerate(materias):
            print(f"- {materia}: {calificaciones[indice]:.2f}")

        print(f"\nPromedio general: {promedio:.2f}")
        print("Umbral de aprobación: 5.00")

        print("\nMaterias aprobadas:")
        if aprobadas:
            for indice in aprobadas:
                print(f"- {materias[indice]}: {calificaciones[indice]:.2f}")
        else:
            print("Ninguna.")

        print("\nMaterias reprobadas:")
        if reprobadas:
            for indice in reprobadas:
                print(f"- {materias[indice]}: {calificaciones[indice]:.2f}")
        else:
            print("Ninguna.")

        print(
            f"\nMateria con mejor calificación: {materias[indice_maximo]} "
            f"({calificaciones[indice_maximo]:.2f})"
        )
        print(
            f"Materia con peor calificación: {materias[indice_minimo]} "
            f"({calificaciones[indice_minimo]:.2f})"
        )

    print("\n¡Gracias por usar la calculadora! Hasta pronto.")


if __name__ == "__main__":
    main()
