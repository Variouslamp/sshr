#!/usr/bin/env python3

# python
import sys

# scripts
from .orchestrator import (
    COMANDOS,  # Diccionario de comandos y sus caracteristicas
    orchestrator_main,  # Orquestador de coneccion con modulos de comandos
    )
from sshr.assistant.error import Error
from sshr.core.internal.validation import validar_flag

# -----------------------------------------------------------------------------
# Definicion de flags y su validacion
# -----------------------------------------------------------------------------

flags_dict = COMANDOS  # diccionario con toda la informacion de los comandos


# -----------------------------------------------------------------------------
# Valida la cantidad de argumentos necesarios para usar un comando especifico


def validar_cantidad(comando: str, num_argumentos: int) -> bool:
    if "max_input_args" in flags_dict[comando]:
        if not (flags_dict[comando]["min_input_args"] <= num_argumentos <= flags_dict[comando]["max_input_args"]):
            Error("ERR014").format(command=comando).print_er()
    elif not (num_argumentos == flags_dict[comando]["input_args"]):
        Error("ERR014").format(command=comando).print_er()
    return True


# -----------------------------------------------------------------------------
# Funcion que ensambla y activa el funcionamiento y validacion de datos
# ingresados por el usuario

def main():
    args = sys.argv[1:]
    num_args = len(args)
    if num_args != 0:
        comando = validar_flag(args[0], flags_dict)
        if not type(comando) is str:
            return Error("ERR012").print_er()
        if validar_cantidad(comando, num_args):
            orchestrator_main(comando, flags_dict, args)
    else:
        Error("ERR013").print_er()


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit(130)
