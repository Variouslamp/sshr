# -----------------------------------------------------------------------------
# Centro de informacion de comandos, las funciones que las ejecutan, flags y
# argumentos necesarios para su correcta ejecucion

COMANDOS = {
    "register": {
        "flags": ["-r", "--register"],
        "used_args": 2,
        "input_args": 2,
        "need_args": ["direccion_conexion", "directorio_ssh"],
    },
    "edit": {
        "flags": ["-e", "--edit"],
        "used_args": 0,
        "input_args": 1,
        "need_args": [],
    },
    "list": {
        "flags": ["-l", "-ll", "--list"],
        "used_args": 2,
        "input_args": 1,
        "need_args": ["directorio_ssh", "flag"],
    },
    "delete": {
        "flags": ["-d", "--delete"],
        "used_args": 1,
        "input_args": 1,
        "need_args": ["directorio_ssh"],
    },
    "build": {
        "flags": ["build"],
        "used_args": 0,
        "input_args": 1,
        "need_args": [],
    },
    "help": {
        "flags": ["-h", "--help"],
        "used_args": 1,
        "max_input_args": 2,
        "min_input_args": 1,
        "need_args": ["help_arg"],
    }
}
