#!/usr/bin/env python3

# python
import subprocess
import sys
# scripts
from commands.registrar import register_main 

# ---------------------------------------------------------------
# Definicion de flags y su validacion
# ---------------------------------------------------------------

COMANDOS = {
    "register":{
        "function":"",
        "flags": ["-r", "--register"]},
    "edit":{
        "function":"",
        "flags": ["-e", "--edit"]},
    "list":{
        "function":"",
        "flags": ["-l", "--list"]},
    "delete":{
        "function":"",
        "flags": ["-d", "--delete"]},
}

def validar_flag(flag: str, diccionario: dict) -> bool:
    for comando in diccionario:
        if comando[0] in flag:
            flag_list =  diccionario[comando]["flags"]
            if flag in flag_list:
                return True
    return False
   

# ---------------------------------------------------------------

def cli_input(argumentos: tuple):
    num_argumentos  = len(argumentos)
    if num_argumentos == 0:
            print("sshr error: Menos argumentos de los esperados")
    elif num_argumentos == 1:
        arg = argumentos[0]
        if validar_flag(arg, COMANDOS):
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
                    print(f"Error: Argumento '{arg}' no identificado")
        else:
            print("Error: ")

# ---------------------------------------------------------------

    elif num_argumentos == 2:
        if validar_flag(argumentos[0], COMANDOS):
            flag = argumentos[0]
            addr = argumentos[1]
            match flag:
                case "-r":
                    register_main(addr)
                case _:
                    print("flag invalida para uso con direccion")
        else:
            print("Error: estructura de mensaje no reconocida")
    else: 
        print("sshr error: Mas agrumentos de los esperados")

# ---------------------------------------------------------------
# Entrada a la herramienta CLI

def main():
    args = sys.argv[1:]
    cli_input(args)

# ---------------------------------------------------------------

main()
