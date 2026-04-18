def deteccion_componentes(argumento):
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
        direccion["ip"] = f"{seccs[0]}"
    if num_seccs >= 2:
        direccion["user" if is_arr else "port"] = f"{seccs[1]}"
    if num_seccs == 3:
        direccion["port"] = f"{seccs[2]}"

    # ---- Reglas basicas de puerto -----

    if "port" not in direccion:
        direccion["port"] = 22
    else:
        try:
            int(direccion["port"])
        except:
            return print("Error: puerto invalido no numerico")

    return direccion  # Retorno de diccionario organizado


# -- input de prueba --
# print(deteccion_componentes(input("> ")))
