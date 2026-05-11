# -----------------------------------------------------------------------------

from pathlib import Path
import json  # Manejo de informacion de ayuda en el json


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
    def __init__(self, command: str):
        self.dict = self._get_dict()
        self.text = self._get_text()

    def print_help(self):
        print(self.text)

    def _get_dict(self):
        with open(HELPS_JSON, "r") as f:
            help_dict = json.load(f)
        return help_dict

    def _get_text(self) -> dict:
        -------- # Separadores temporales de lo que se cambiara
        raw = self._raw_text()
        components = []
        for _title, i in raw.items():
            components.append(i)
        text = "\n".join(components)
        return text
        ---------

    def _raw_text(self) -> dict:
        for section, content in self.dict.items():
            if self.error in content:
                return content[self.error]

#a = Help()