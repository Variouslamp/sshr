# herramientas
from pathlib import Path
import configparser
from sshr.core.internal.flags import COMANDOS

# funciones
from sshr.commands.register import register_main  # funcion de registro
from sshr.commands.list import list_main  # funcion de listado
from sshr.commands.delete import delete_main  # funcion de eliminacion
from sshr.commands.edit import edit_main  # funcion de edicion de registros
from sshr.commands.build import build_main  # funcion de edicion de registros
from sshr.assistant.help.help_command import help_main  # funcion para documentacion


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
    ejecutar_funcion(comando, argumentos_entregar, FUNCIONES)
