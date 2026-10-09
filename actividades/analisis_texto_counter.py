"""Análisis de frecuencias de caracteres utilizando Counter."""

from collections import Counter


def analizar_texto(texto):
    """Devuelve frecuencias y totales, excluyendo blancos del conteo parcial."""
    # isspace() identifica espacios, tabulaciones y saltos de línea.
    sin_espacios = [caracter for caracter in texto if not caracter.isspace()]
    frecuencias = Counter(sin_espacios)

    return {
        "caracteres_mas_comunes": frecuencias.most_common(3),
        "total_caracteres": len(texto),
        "total_sin_espacios": len(sin_espacios),
    }


if __name__ == "__main__":
    resultado = analizar_texto("Hola, mundo! Este es un ejemplo.")
    print(resultado)
