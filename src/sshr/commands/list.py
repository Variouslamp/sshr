# -----------------------------------------------------------------------------
# Funcion que permite obtener lista de conecciones y dividirlas en secciones
# (Tambien se utiliza en el modulo delete (tener cuidado al editar))


def entrega_texto(archivo_ssh: str) -> list:
    with open(archivo_ssh, "r")as f:
        archivo = f.read()
    return archivo


# -----------------------------------------------------------------------------
# Funcion que que extrae las conexiones del archivo config y las entrega ordenadas


def obtener_conexiones(archivo_ssh: str) -> list:
    conexiones = (entrega_texto(archivo_ssh)).split("\n\n")
    lista_ordenada = []
    for conexion in conexiones:
        if not conexion:
            conexiones.remove(conexion)
        else:
            lista_ordenada.append(conexion.replace("    ", ""))
    return (lista_ordenada)


# -----------------------------------------------------------------------------
# Funcion la cual imprime todas las conexiones en formato de lista larga


def imprimir_lista_larga(lista_ordenada: list):
    numero = 0
    for registro in lista_ordenada:
        numero += 1
        print(f"\n[{numero}]")
        registro = (registro
                    .replace("HostName", "ip:")
                    .replace("Host", "Name:")
                    .replace("User", "User:")
                    .replace("Port", "Port:"))
        print(registro)


# -----------------------------------------------------------------------------
# Funcion la cual imprime todas las conexiones en formato de lista larga


def imprimir_lista_corta(lista):
    contador = 1
    for bloque in lista:
        datos = {}
        for linea in bloque.strip().splitlines():
            partes = linea.split(None, 1)
            if len(partes) == 2:
                datos[partes[0]] = partes[1]

        if "Host" not in datos:
            continue

        host = datos.get("Host", "desconocido")
        hostname = datos.get("HostName", "")
        user = datos.get("User", "")
        port = datos.get("Port", "")
        direccion = hostname
        if user:
            direccion = f"{user}@{direccion}"
        if port:
            direccion = f"{direccion}:{port}"
        print(f"[{contador}] {host} - {direccion}")
        contador += 1

# -----------------------------------------------------------------------------
# Funcion principal de listado de los registros


def list_main(flag: str, archivo_ssh: str):
    lista = obtener_conexiones(archivo_ssh)
    match flag:
        case "-ll":
            imprimir_lista_larga(lista)
        case _:
            imprimir_lista_corta(lista)
