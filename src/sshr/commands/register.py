# importaciones

from sshr.core.internal.validation import validator
from sshr.assistant.error import Error


# -----------------------------------------------------------------------------

def parseo_de_direccion(argumento: str) -> dict:
    direccion = {}  # Diccionario de almacenamiento de datos procesados

    # -----Deteccion de simbolos y su cantidad -----------

    is_arr = (True if "@" in argumento else False)
    if is_arr:
        num_arr = argumento.count("@")
        if num_arr > 1:
            return Error("ERR001").format(value=argumento).print_er()
    is_dp = (True if ":" in argumento else False)
    if is_dp:
        num_dp = argumento.count(":")
        if num_dp > 1:
            return Error("ERR002").format(value=argumento).print_er()

    # ---- Divicion de segmentos de la direccion -----------------

    seccs = list(argumento.replace("@", ":").split(":"))
    for secc in seccs:
        if not secc:
            return Error("ERR003").format(value=argumento).print_er()
    if is_arr and is_dp:
        arr_sec = argumento.split("@")
        dp_sec = argumento.split(":")
        if ":" in arr_sec[0]:
            return Error("ERR004").format(value=argumento).print_er()
        if "@" in dp_sec[1]:
            return Error("ERR005").format(value=argumento).print_er()
    elif is_arr:
        arr_sec = argumento.split("@")

    # ---- Organizacion de secciones ----

    if is_arr:
        seccs[0], seccs[1] = seccs[1], seccs[0]

    # ---- Almacenamiento de secciones independientes -----

    num_seccs = len(seccs)

    if num_seccs >= 1:
        direccion["HostName"] = f"{seccs[0]}"
    if num_seccs >= 2:
        direccion["User" if is_arr else "Port"] = f"{seccs[1]}"
    if num_seccs == 3:
        direccion["Port"] = f"{seccs[2]}"

    # ---- Reglas basicas de puerto -----

    if "Port" not in direccion:
        direccion["Port"] = 22
    else:
        try:
            int(direccion["Port"])
        except ValueError:
            return Error("ERR006").print_er()

    return direccion  # Retorno de diccionario organizado


# -----------------------------------------------------------------------------
# Funcion que valida que no se ingresen nombres repetidos en las conecciones

def name_exist(selected_name: str, ssh_file: str):
    names = []
    with open(ssh_file, "r")as file:
        for line in file:
            if "Host " in line:
                register_name = ((line.strip().split(" "))[1]).replace("\n", " ")
                names.append(register_name)
        for name in names:
            if selected_name == name:
                return True
    return False

# -----------------------------------------------------------------------------
# Funcion que se encarga del almacenamiento de alias para poder usarlo como
# alias en una conexion de ssh


def agregar_alias(diccionario: dict, ssh_file: str) -> dict:
    while True:

        exit = False
        guardar = ""
        alias = ""

        alias = input("- What's the alias for this conection? -> ")
        print(f"Selected alias: {alias}")
        if name_exist(alias, ssh_file):
            Error("ERR007").format(name=alias).print_er()
            continue
        while guardar != 1:
            print("\nSelec an option to continua")
            print(f"- 1 to store the conection with '{alias}' alias")
            print("- 2 to edit the alias")
            print("- 0 to cancel the process")
            while True:
                guardar = validator(int, "> ")
                if guardar == 1:
                    print(f"Stored alias -> {alias}")
                    exit = True
                    break
                elif guardar == 2:
                    guardar = 1
                    break
                elif guardar == 0:
                    print("Saliendo...")
                    return None
                if exit:
                    break
        if exit:
            break
    diccionario["Host"] = alias
    return diccionario

# -----------------------------------------------------------------------------
# Funciond de creacion de texto para el documento


def agregar_conexion(datos: dict) -> str:
    campos_disponibles = ["Host", "HostName", "User", "Port"]

    lineas = [""]

    for campo in campos_disponibles:
        if campo in datos:
            valor = datos[campo]
            sangria = "" if campo == "Host" else "    "
            lineas.append(f"{sangria}{campo} {valor}")

    return "\n".join(lineas)

# -----------------------------------------------------------------------------
# Funcion principal de la funcion de registro de direcciones


def register_main(direccion_conexion: str, ssh_file: str):
    diccionario_direccion = parseo_de_direccion(direccion_conexion)
    if diccionario_direccion:
        diccionario_almacenar = agregar_alias(diccionario_direccion, ssh_file)
        if diccionario_almacenar is None:
            return
        texto_configuracion = agregar_conexion(diccionario_almacenar)
        with open(ssh_file, "a") as f:
            f.write(f"{texto_configuracion}\n")
