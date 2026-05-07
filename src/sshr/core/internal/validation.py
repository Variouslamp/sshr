"""
    Archivo que se enfoca en el alamcenamiento de funciones que se usan de
    de manera consistente en los demas modulos del proyecto.
    Enfocado en validacion de datos o inputs
"""

# -----------------------------------------------------------------------------
# Funcion enfocada en la validacion de valores de input del usuario teniendo en
# cuenta un tipo especifico de valor esperado y un mensaje 

from sshr.assistant.error import Error


def validator(type: type, text: str = "", error_text: str = None) -> type: # retorna el type que se ingreso
    while True:
        try:
            data = type(input(text))
            return data
        except ValueError:
            Error("ERR011").format(type=type).print_er()
            continue