"""
    Archivo que se enfoca en el alamcenamiento de funciones que se usan de
    de manera consistente en los demas modulos del proyecto.
    Enfocado en validacion de datos o inputs
"""

# -----------------------------------------------------------------------------
# Funcion enfocada en la validacion de valores de input del usuario teniendo en
# cuenta un tipo especifico de valor esperado y un mensaje 

from sshr.assistant.error import Error


def validator(type: type, text: str = "") -> type: # retorna el type que se ingreso
    while True:
        try:
            data = type(input(text))
            return data
        except ValueError:
            Error("ERR011").format(type=type).print_er()
            continue


# -----------------------------------------------------------------------------
# Validador de  entrada de flags y si hace parte de una de las flags definidas
# en el diccionario que se le pase a la funcion

# Ingreso de una flag y su validacion segun diccionario de flags
def validar_flag(flag: str, diccionario: dict) -> bool:
    for comando in diccionario:
        if comando[0] in flag:
            flag_list = diccionario[comando]["flags"]
            if flag in flag_list:
                return comando
    return False
