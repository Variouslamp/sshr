# -----------------------------------------------------------------------------

from pathlib import Path
import json  # Manejo de informacion de ayuda en el json

# Importaciones de otros modulos internos
from sshr.core.internal.validation import validar_flag
from sshr.assistant.error.error_handler import Error   # Clase para hallar errores
from sshr.core.internal.flags import COMANDOS

# -----------------------------------------------------------------------------
# Diccionario que define flags validas

flags_dict = COMANDOS  # diccionario con toda la informacion de los comandos

# -----------------------------------------------------------------------------
# Directorio donde se encuentra el archivo con informacion de mensajes de ayuda


HELPS_JSON = Path(__file__).parent / "help.json"


# -----------------------------------------------------------------------------
# Error que se levanta si el comando de ayuda no existe

class ErrorValueOutOfRange(Exception):
    pass

# -----------------------------------------------------------------------------
# Clase encargada del manejo de ayuda e impresion


class Help():
    def __init__(self, section: str, help_command: str = None):
        self.dict = self._get_dict()
        self.text = self._get_text(section, help_command)

    def print_help(self):
        print(f"\n{self.text}")

    def _get_dict(self):
        with open(HELPS_JSON, "r") as f:
            help_dict = json.load(f)
        return help_dict

    def _get_text(self, section, help_command: str = None) -> dict:
        raw = self._raw_text(section, help_command)
        return raw

    def _raw_text(self, section: str, help_command: str = None) -> str:
        text = []
        if section == "general":
            for value in self.dict["general"]:
                if value == "commands":
                    for line in self.dict["general"]["commands"]:
                        text.append(line)
                    continue
                text.append(self.dict["general"][value])
            help_text = "\n".join(text)
            return help_text

        elif section == "commands":
            for command in self.dict["commands"]:
                if command != help_command:
                    continue
                for value in self.dict["commands"][help_command]:
                    text.append(self.dict["commands"][help_command][value])
            help_text = "\n".join(text)
            return help_text


# -----------------------------------------------------------------------------
# Clase que hereda de la clase de assistant/error/error_handler para la lectura
# del archivo de errores donde se encuentra los mensaje de ayuda de los errores


class PrntErrorHelp(Error):
    def _get_text(self) -> dict:
        raw = self._raw_text(self.error)
        if raw is None:
            return None
        components = []
        for _title, i in raw.items():
            if _title != "help":  # Exepciones de contenido a no imprimir
                continue
            for _, line in raw[_title].items():
                components.append(line)
        components.append("\n")
        text = "\n".join(components)
        return text

    def _validator(self, code_error):
        final_section = next(reversed(self.dict))
        final_code = next(reversed(self.dict[final_section]))
        raw_code = (final_code.split("ERR"))[1]
        if "ERR" in code_error:
            try:
                if int((code_error.split("ERR"))[1]) <= int(raw_code):
                    return code_error
            except:
                return None
            return code_error

    def _raw_text(self, Error_code) -> dict:
        if Error_code is None:
            return None
        """Finds and returns the error entry across all JSON sections."""
        for _, content in self.dict.items():
            if self.error in content:
                return content[self.error]


# -----------------------------------------------------------------------------


def help_main(help_arg: str):
    if help_arg is None:
        Help("general").print_help()
    else:
        error_object = PrntErrorHelp(help_arg)
        if "ERR" in help_arg:
            if error_object.text is None:
                Error("ERR015").format(code=help_arg).print_er()
            else:
                error_object.print_er()
        else:
            comando = validar_flag(help_arg, flags_dict)
            if not comando:
                Error("ERR016").format(command=help_arg).print_er()
                return
            Help("commands", comando).print_help()
