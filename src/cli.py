#!/usr/bin/env python3

# python
import subprocess
import sys
# scripts
from registrar import deteccion_componentes 


args = sys.argv


def is_flag(flag):
    if "-" in flag[0] and type(flag) is str:
        return True
    return False

# ----------------Acciones del archivo de config-------------------------

def cli_input(argumentos):
    num_argumentos  = len(args)
    if num_argumentos == 2:
        arg = argumentos[1]
        if is_flag(arg):
            match arg:
                case "-l":
                    print("lista")
                case "-e":
                    print("Edicion")
                case "-d":
                    print("eliminar")
                case "-r":
                    print("Error: flantan argumentos '-r <direccion>'")
                case _:
                    print(f"Argumento '{arg}' no identificado")
        else:
            subprocess.run(["ssh", f"{arg}"]) # No se que tan buena idea sea esto(probablemente lo cambiare)

# --------------- reguistro de direcciones ------------------

    elif num_argumentos == 3:
        if is_flag(argumentos[1]):
            flag = argumentos[1]
            addr = argumentos[2]
            match flag:
                case "-r":
                    print(deteccion_componentes(addr))
                case _:
                    print("flag invalida para uso con direccion")
        else:
            print("Error: estructura de mensaje no reconocida")
    else:
        if num_argumentos == 1:
            print("sshr error: Menos argumentos de los esperados")
        else:
            print("sshr error: Mas agrumentos de los esperados")

# ---------------------------------------------------------------

cli_input(args)
