# -----------------------------------------------------------------------------

from pathlib import Path
import json  # Manejo de informacion de error en el json


# -----------------------------------------------------------------------------
# Directorio donde se encuentra el archivo de errores


ERRORS_JSON = Path(__file__).parent / "errors.json"


# -----------------------------------------------------------------------------
# Error que se levanta si el codigo de error es invalido

class ErrorValueOutOfRange(Exception):
    pass

# -----------------------------------------------------------------------------
# Clase encargada del manejo de errores, impresion y ejecucion


class Error():
    def __init__(self, code: str):
        """Loads the JSON, validates the error code and prepares the text."""
        self.dict = self._get_dict()
        self.error = self._validator(code)
        self.text = self._get_text()

    def print_er(self):
        """Prints the formatted error with code, description and help text."""
        print(self.text)

    def _get_dict(self):
        """Loads and returns the errors.json file as a dictionary."""
        with open(ERRORS_JSON, "r") as f:
            err_dict = json.load(f)
        return err_dict

    def _get_text(self) -> dict:
        """Builds the error string from message and help fields."""
        raw = self._raw_text()
        components = []
        for _title, i in raw.items():
            components.append(i)
        text = "\n".join(components)
        return text

    def _raw_text(self) -> dict:
        """Finds and returns the error entry across all JSON sections."""
        for section, content in self.dict.items():
            if self.error in content:
                return content[self.error]

    def _validator(self, code_error):
        """Validates the error code is within the JSON range."""
        final_section = next(reversed(self.dict))
        final_code = next(reversed(self.dict[final_section]))
        raw_code = (final_code.split("ERR"))[1]
        if int((code_error.split("ERR"))[1]) <= int(raw_code):
            return code_error
        raise ErrorValueOutOfRange("The error code does not exist in errors.json")

    def format(self, **kwargs):
        """Interpolates placeholders with kwargs. Returns self for chaining."""
        self.text = self.text.format(**kwargs)
        return self



# -----------------------------------------------------------------------------