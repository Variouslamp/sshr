# herramientas
from pathlib import Path
import configparser
from sshr.core.internal.flags import COMANDOS
import sys

# funciones
from sshr.commands.register import register_main  # funcion de registro
from sshr.commands.list import list_main  # funcion de listado
from sshr.commands.delete import delete_main  # funcion de eliminacion
from sshr.commands.edit import edit_main  # funcion de edicion de registros
from sshr.commands.build import build_main  # funcion de edicion de registros
from sshr.assistant.help.help_command import help_main  # funcion para documentacion
from sshr.assistant.error import Error # Gestor de errores en ejecucion

# -----------------------------------------------------------------------------
# Diccionario de funciones para la redireccion a diversos modulos

FUNCIONES = {
    "register": register_main,
    "edit": edit_main,
    "list": list_main,
    "delete": delete_main,
    "build": build_main,
    "help": help_main,
}

# -----------------------------------------------------------------------------
# Seleccion de archivo de configuracion (Tengo que cambiar la logica (creo))


def config_file():
    BASE_DIR = Path(__file__).parent

    dir_config_default = (BASE_DIR / "../templates/config.ini").resolve()
    dir_config_manual = Path("~/.config/sshr/config.ini").expanduser()

    if dir_config_manual.exists():
        return dir_config_manual
    else:
        return dir_config_default


# -----------------------------------------------------------------------------
# respecto a la inforacion entregada por el usuario se extrae los argumentos
# necesarios para entregarle a la respectiva funcion


def obtener_argumentos(
        comando: str,
        diccionario_comandos: dict,
        directorio_ssh: str,
        argumentos: tuple) -> list:

    # Lista vacia en la que se agregaran los argumentos validos que nececita el comando
    argumentos_entregar = []

    # Obtiene la lista que define los argumentos que nececita el comando ejecutado
    argumentos_necesarios = diccionario_comandos[comando]["need_args"]

    # Bucle el cual agrega a la lista "argumentos_entregar" los distintos argumentos
    # necesarios para que el comando ejecutado pueda hacer su trabajo
    for campo in argumentos_necesarios:
        # Dependiendo de cual sea el campo ingresa a un case en el que una funcion le entregara la informacion
        # que corresponda al argumento
        match campo:
            case "direccion_conexion":
                argumentos_entregar.append(argumentos[1])
            case "directorio_ssh":
                # Busca entre las direcciones definidas en "diccionario_direcciones"
                # Donde si alguno de los archivos de ssh existen se retorna dicha direccion
                archivo = Path(f"{directorio_ssh}/config").expanduser()
                if archivo.exists():
                    argumentos_entregar.append(archivo)
                    break
                # si no hay una archivo de ssh de detiene el programa y se levanta un error que explica el porque 
                Error("ERR017").print_er()
                sys.exit(1)
            case "flag":
                # Retorna la flag del commando que se intenta ejecutar por el usuario
                argumentos_entregar.append(argumentos[0])
            case "help_arg":
                if len(argumentos) == 2:
                    argumentos_entregar.append(argumentos[1])
                else:
                    argumentos_entregar.append(None)
            case _:
                # Error interno de desarrollo - campo sin caso en match
                return print("Error: campo no esta en direcciones")
    return argumentos_entregar


# -----------------------------------------------------------------------------
# Funcion dque llama la ejecucion de un comando especifico y entrega sus
# argumentos


def ejecutar_funcion(
        comando: str,
        argumentos: tuple,
        diccionario_funciones: dict):

    funcion = diccionario_funciones[comando]
    funcion(*argumentos)


# -----------------------------------------------------------------------------
# Funcion principal de orquestamiento de las funciones

def orchestrator_main(
        comando: str, diccionario_comandos: dict, argumentos: tuple
        ):

    config = configparser.ConfigParser()
    config.read(config_file())

    directorio_ssh = config["directory"]["SSH_DIR"]

    argumentos_entregar = obtener_argumentos(
        comando,
        diccionario_comandos,
        directorio_ssh,
        argumentos
        )
    ejecutar_funcion(comando, argumentos_entregar, FUNCIONES)
