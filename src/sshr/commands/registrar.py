def parseo_de_direccion(argumento: str) -> dict :
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
        except:
            return print("Error: puerto invalido no numerico")

    return direccion  # Retorno de diccionario organizado

# -----------------------------------------------------------

def agregar_alias(diccionario: dict) -> dict:
    while True:

        exit = False
        selec = ""
        guardar = ""
        alias = ""

        alias = input("- What's the alias for this conection? -> ")
        print(f"Selected alias -> {alias}")
        while len(selec) == 0:
            guardar = input("are you sure? [y/n]: ").lower().strip()
            if guardar in ["y","Yes"]:
                print(f"Stored alias -> {alias}")
                exit = True
                break
            elif guardar in ["n","no"]:
                while True:
                    print("\n- press 1 if you want to change the alias")
                    print("- press 0 if you want to exit")
                    selec = input(">> ").strip() 
                    if selec == "1": 
                        break
                    elif selec == "0":
                        return None
            if exit:
                break
        if exit:
            break
    diccionario["Host"] = alias
    return diccionario
                    
# ------------------------------------------------
# Funciond de creacion de texto para el documento

def agregar_conexion(datos: dict) -> str:
    campos_disponibles = ["Host", "HostName", "User", "Port"]
    
    lineas = [" ",]
    
    for campo in campos_disponibles:
        if campo in datos:
            valor = datos[campo]
            sangria = "" if campo == "Host" else "    "
            lineas.append(f"{sangria}{campo} {valor}")
    
    return "\n".join(lineas)


#-------- Funcion de registro de direcciones------

def register_main(argumentos: str):
    dic = agregar_alias(parseo_de_direccion(argumentos))
    tx = agregar_conexion(dic)
    with open("/home/various/projects-dev/sshr/src/sshr/texto", "a") as f:
        f.write(tx)
