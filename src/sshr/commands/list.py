# -----------------------------------------------------------------------------
# Funcion que permite obtener lista de conecciones y dividirlas en secciones


def obtener_conexiones(archivo_ssh: str) -> list:
    with archivo_ssh.open('r') as f:
        archivo = f.read()
        conexiones = archivo.split(" \n")
        lista_ordenada = []
        for conexion in conexiones:
            if not conexion:
                conexiones.remove(conexion)
            else:
                lista_ordenada.append(conexion.replace("    ", ""))
        return (lista_ordenada)


# -----------------------------------------------------------------------------


def imprimir_lista_larga(lista_ordenada: list):
    numero = 0
    for registro in lista_ordenada:
        numero += 1
        print(f"#{numero} ---")
        registro = (registro
                    .replace("HostName", "ip:")
                    .replace("Host", "Name:")
                    .replace("User", "User:")
                    .replace("Port", "Port:"))
        print(registro)


# -----------------------------------------------------------------------------


def mostrar_hosts(lista):
    for i, bloque in enumerate(lista, start=1):
        datos = {}
        for linea in bloque.strip().splitlines():
            partes = linea.split(None, 1)
            if len(partes) == 2:
                datos[partes[0]] = partes[1]

        host = datos.get("Host", "desconocido")
        hostname = datos.get("HostName", "")
        user = datos.get("User", "")
        port = datos.get("Port", "")

        direccion = hostname
        if user:
            direccion = f"{user}@{direccion}"
        if port:
            direccion = f"{direccion}:{port}"

        print(f"#{i} - {host} - {direccion}")

# -----------------------------------------------------------------------------
# Funcion principal de listado de los registros


def list_main(flag: str, archivo_ssh: str):
    lista = obtener_conexiones(archivo_ssh)
    match flag:
        case "-ll":
            imprimir_lista_larga(lista)
        case _:
            mostrar_hosts(lista)
