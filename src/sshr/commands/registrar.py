def parseo_de_direccion(argumento: str) -> dict:
    direccion = {}  # Diccionario de almacenamiento de datos procesados

    # -----Deteccion de simbolos y su cantidad -----------

    is_arr = (True if "@" in argumento else False)
    if is_arr:
        num_arr = argumento.count("@")
        if num_arr > 1:
            return print(
                f"Error: mas simbolos '@' de los necesarios en '{argumento}'")
    is_dp = (True if ":" in argumento else False)
    if is_dp:
        num_dp = argumento.count(":")
        if num_dp > 1:
            return print(f"Error: mas simbolos ':' en '{argumento}'")

    # ---- Divicion de segmentos de la direccion -----------------

    seccs = list(argumento.replace("@", ":").split(":"))
    for secc in seccs:
        if not secc:
            return print(
                f"Error: Argumentos faltantes en la direccion: '{argumento}'")
    if is_arr and is_dp:
        arr_sec = argumento.split("@")
        dp_sec = argumento.split(":")
        if ":" in arr_sec[0]:
            return print(
                f"Error: Orden de los argumentos de direccion erroneo '{argumento}', : detras de @")
        if "@" in dp_sec[1]:
            return print(
                f"Error: Orden de los argumentos de direccion erroneo '{argumento}', @ delante de :")
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
            return print("Error: puerto invalido no numerico")

    return direccion  # Retorno de diccionario organizado

# -----------------------------------------------------------------------------
# Funcion que se encarga del almacenamiento de alias para poder usarlo como
# alias en una conexion de ssh


def agregar_alias(diccionario: dict) -> dict:
    while True:

        exit = False
        guardar = ""
        alias = ""

        alias = input("- What's the alias for this conection? -> ")
        print(f"Selected alias: {alias}")
        while guardar != 1:
            print("\nSelec an option to continua")
            print(f"- 1 to store the conection with '{alias}' alias")
            print("- 2 to edit the alias")
            print("- 0 to cancel the process")
            while True:
                try:
                    guardar = int(input("> "))
                except ValueError:
                    print("Error: Selected option is not valid")
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


def register_main(direccion_conexion: str, directorio_ssh: str):
    diccionario_direccion = parseo_de_direccion(direccion_conexion)
    if diccionario_direccion:
        diccionario_almacenar = agregar_alias(diccionario_direccion)
        if diccionario_almacenar is None:
            return
        texto_configuracion = agregar_conexion(diccionario_almacenar)
        with open(directorio_ssh, "a") as f:
            f.write(f"{texto_configuracion}\n")
