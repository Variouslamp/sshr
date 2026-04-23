#!/usr/bin/env python3

# python
import sys

# scripts
from .orchestrator import (
    COMANDOS,  # Diccionario de comandos y sus caracteristicas
    orchestrator_main,  # Orquestador de coneccion con modulos de comandos
    )

# -----------------------------------------------------------------------------
# Definicion de flags y su validacion
# -----------------------------------------------------------------------------

flags_dict = COMANDOS  # diccionario con toda la informacion de los comandos


# Ingreso de una flag y su validacion segun diccionario de flags
def validar_flag(flag: str, diccionario: dict) -> bool:
    for comando in diccionario:
        if comando[0] in flag:
            flag_list = diccionario[comando]["flags"]
            if flag in flag_list:
                return comando
    return False


# -----------------------------------------------------------------------------
# Valida la cantidad de argumentos necesarios para usar un comando especifico


def validar_cantidad(comando: str, num_argumentos: int) -> bool:
    if num_argumentos == flags_dict[comando]["input_args"]:
        return True
    else:
        print(f"Error: Numero de argumentos para la accion <{comando}> ")


# -----------------------------------------------------------------------------
# Funcion que ensambla y activa el funcionamiento y validacion de datos
# ingresados por el usuario

def main():
    args = sys.argv[1:]
    num_args = len(args)
    if num_args != 0:
        comando = validar_flag(args[0], flags_dict)
        if not type(comando) is str:
            return print("Error: Flag no valida")
        if validar_cantidad(comando, num_args):
            orchestrator_main(comando, flags_dict, args)
    else:
        print("Error: Argumentos no ingresados")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit(130)
