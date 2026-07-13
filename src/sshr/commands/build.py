
import configparser
from pathlib import Path
from shutil import copy2
import os

# -----------------------------------------------------------------------------
# Clase enfoca en la impresion de valores para no tener que repetir codigo

class Message():
    def __init__(self, text=None):
        self.text = text

    def pnt_step(self, number):
        print(f"[{number}] {self.text}")

    def pnt_info(self):
        print(f"    ├─ [INFO] {self.text}")

    def pnt_found(self):
        print(f"    ├─ [FOUND] {self.text}")

    def pnt_crea(self):
        print(f"    ├─ [CREATED] {self.text}")

    def pnt_warn(self):
        print(f"    ├─ [WARNING] {self.text}")

    def pnt_done(self):
        print("    └─ [DONE] \n")

    def pnt_end(self):
        print(self.text)


# -----------------------------------------------------------------------------
# Funcion que obtiene una direcion valida donde se puede encontrar la carpeta
# de sshr


def get_config_dir(home_dir, xdg_dir):
    # Si la ruta de de configuracion no esta definida se usara la ruta comun
    # de $HOME/.config/
    if xdg_dir:
        direccion_config = Path(xdg_dir)
        Message(f"Global configuration directory found in ({direccion_config})").pnt_found()
        return direccion_config
    direccion_config = home_dir / ".config"
    if direccion_config.exists():
        Message(f"Global configuration directory found in ({direccion_config})").pnt_found()
        return direccion_config
    Message("Configuration directory was not found").pnt_warn()
    Message(f"Creating new configuration directory ({home_dir}/.config)").pnt_info()
    direccion_config = home_dir / ".config"
    direccion_config.mkdir()
    Message("configuration directory was successfully created").pnt_crea()
    return direccion_config

# -----------------------------------------------------------------------------
# Funcion que busca o crea el directorio de configuracion de sshr

def found_create_sshr_config(direccion_config):
    direccion_sshr = direccion_config / "sshr"
    if direccion_sshr.exists():
        Message(f"sshr configuration directory found in ({direccion_sshr})").pnt_found()
        return direccion_sshr
    Message("sshr configuration directory was not found").pnt_warn()
    Message(f"Creating sshr configuration directory ({direccion_sshr})").pnt_info()
    direccion_sshr.mkdir()
    Message("sshr directory was successfully created").pnt_crea()
    return direccion_sshr


# -----------------------------------------------------------------------------
# Funcion enfocada en buscar archivo de configuracion y extraer su contenido

def get_configuration_file(direccion_sshr, project_dir):
    config_file = direccion_sshr / "config.ini"
    if config_file.exists() and config_file.is_file():
        Message(f"Configuration file found in ({config_file})").pnt_found()
        return config_file
    Message("Configuration file was not found").pnt_warn()
    Message(f"Adding default configuration file to ({direccion_sshr})").pnt_info()
    config_template = project_dir / "templates/config.ini"
    copy2(config_template, direccion_sshr)
    Message("Default configuration file was successfully added in configuration directory").pnt_crea()
    return config_file


# -----------------------------------------------------------------------------
# Funcion enfocada en buscar el archivo .ssh con la informacion plasmada en el config.ini


def get_ssh_directory(config_file):
    Message("Reading 'config.ini' file to extract the ssh directory path").pnt_info()
    config = configparser.ConfigParser()
    config.read(config_file)
    ssh_dir = Path(config["directory"]["SSH_DIR"]).expanduser()
    Message("ssh directory path was successfully extracted from the config file").pnt_info()
    Message("Checking if directory path exists...").pnt_info()
    if ssh_dir.exists():
        Message(f"ssh directory was successfully located in ({ssh_dir})").pnt_found()
        return ssh_dir
    Message("ssh directory couldn't be located").pnt_warn()
    Message(f"Creating ssh directory in ({ssh_dir})").pnt_info()
    ssh_dir.mkdir()
    Message(".ssh directory was successfully created").pnt_crea()
    return ssh_dir

# -----------------------------------------------------------------------------
# Funcion enfocada en buscar el archivo .ssh con la informacion plasmada en el config.ini


def get_ssh_config_file(ssh_dir):
    ssh_config_file = ssh_dir / "config"
    if ssh_config_file.exists() and ssh_config_file.is_file():
        Message(f"ssh configuration file was found in ({ssh_config_file})").pnt_found()
        return ssh_config_file
    Message("ssh configuration file was not found").pnt_warn()
    Message(f"Adding an ssh configuration file to ({ssh_config_file})").pnt_info()
    ssh_config_file.touch()
    Message("Blank configuration file was successfully added in .ssh directory").pnt_crea()
    return ssh_config_file


# -----------------------------------------------------------------------------
# Funcion principal de construccion de carpetas y directorios

def build_main():

    # Obtencion de las variables de entorno para identifica el directorio conf
    home = Path(os.getenv("HOME"))
    xdg = os.getenv("XDG_CONFIG_HOME")
    PROJECT_DIR = Path(__file__).resolve().parent.parent

    print("="*6 + " BUILD " + "="*6 + "\n")
    Message("Searching global configuration directory...").pnt_step(1)
    direccion_config = get_config_dir(home, xdg)
    Message().pnt_done()
    Message("Searching for sshr configuration directory in global configuration directory...").pnt_step(2)
    direccion_sshr = found_create_sshr_config(direccion_config)
    Message().pnt_done()
    Message(f"Searching for sshr configuration file 'config.ini' in ({direccion_sshr})...").pnt_step(3)
    config_file = get_configuration_file(direccion_sshr, PROJECT_DIR)
    Message().pnt_done()
    Message("Searching for .ssh directory based on sshr config.ini file...").pnt_step(4)
    ssh_dir = get_ssh_directory(config_file)
    Message().pnt_done()
    Message("Searching for config file in .ssh to store the aliases...").pnt_step(5)
    get_ssh_config_file(ssh_dir)
    Message().pnt_done()
    print("== BUILD PROCESS IS DONE ==")
