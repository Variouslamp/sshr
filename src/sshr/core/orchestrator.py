# herramientas
from pathlib import Path
import configparser

# funciones
from sshr.commands.register import register_main  # funcion de registro
from sshr.commands.list import list_main  # funcion de listado
from sshr.commands.delete import delete_main  # funcion de eliminacion
from sshr.commands.edit import edit_main  # funcion de edicion de registros
from sshr.commands.build import build_main  # funcion de edicion de registros


# -----------------------------------------------------------------------------
# Centro de informacion de comandos, las funciones que las ejecutan, flags y
# argumentos necesarios para su correcta ejecucion

COMANDOS = {
    "register": {
        "function": register_main,  # funcion que ejecuta ese comando
        "flags": ["-r", "--register"],  # flags que activan ese comando
        "used_args": 2,  # Num argumentos que nececita el comando pra funcionar
        "input_args": 2,  # Num argumentos que entrega el usuario en la CLI
        # tienen que ser entregadas en este mismmo orde a la funcion
        "need_args": ["direccion_conexion", "directorio_ssh"],
        },
    "edit": {
        "function": edit_main,
        "flags": ["-e", "--edit"],
        "used_args": 0,
        "input_args": 1,
        "need_args": [],
        },
    "list": {
        "function": list_main,
        "flags": ["-l", "-ll", "--list"],
        "used_args": 2,
        "input_args": 1,
        "need_args": ["directorio_ssh", "flag"],
        },
    "delete": {
        "function": delete_main,
        "flags": ["-d", "--delete"],
        "used_args": 1,
        "input_args": 1,
        "need_args": ["directorio_ssh"],
        },
    "build": {
        "function": build_main,
        "flags": ["build"],
        "used_args": 0,
        "input_args": 1,
        "need_args": [],
        }
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
        diccionario_direcciones: dict,
        argumentos: tuple) -> list:

    argumentos_entregar = []
    argumentos_necesarios = diccionario_comandos[comando]["need_args"]
    for campo in argumentos_necesarios:
        match campo:
            case "direccion_conexion":
                argumentos_entregar.append(argumentos[1])
            case "directorio_ssh":
                for direccion_ssh in diccionario_direcciones[campo]:
                    archivo = Path(f"{direccion_ssh}/config").expanduser()
                    if archivo.exists():
                        argumentos_entregar.append(archivo)
                        break
            case "flag":
                argumentos_entregar.append(argumentos[0])
            case _:
                return print("Error: campo no esta en direcciones")
    return argumentos_entregar


# -----------------------------------------------------------------------------
# Funcion dque llama la ejecucion de un comando especifico y entrega sus
# argumentos


def ejecutar_funcion(
        comando: str,
        argumentos: tuple,
        diccionario_comandos: dict):

    funcion = diccionario_comandos[comando]["function"]
    funcion(*argumentos)


# -----------------------------------------------------------------------------
# Funcion principal de orquestamiento de las funciones

def orchestrator_main(
        comando: str,
        diccionario_comandos: dict,
        argumentos: tuple,
        ):

    config = configparser.ConfigParser()
    config.read(config_file())

    DIRECCIONES = {
        "directorio_ssh": [config["directory"]["SSH_DIR"], "~/projects-dev/sshr/src/sshr/templates/"],
        "direccion_config": [],
    }

    argumentos_entregar = obtener_argumentos(
        comando,
        diccionario_comandos,
        DIRECCIONES,
        argumentos
        )
    ejecutar_funcion(comando, argumentos_entregar, diccionario_comandos)
