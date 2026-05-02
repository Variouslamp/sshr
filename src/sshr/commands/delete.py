from .list import list_main # Importa impresion de lista

# -----------------------------------------------------------------------------
# Funcion que parsea y ordena las lineas en un diccionario


def get_text(ssh_file: str) -> list:
    lines = []
    with open(ssh_file, "r")as file:
        for line in file:
            lines.append(line)
        return lines


# -----------------------------------------------------------------------------
# Funcion de validador de inputs


def validator(text: str, type: type) -> type: # retorna el type que se ingreso
    while True:
        try:
            data = type(input(text))
            return data
        except ValueError:
            print(f"Error: Given value is invalid just {type} value accepted")
            continue


# -----------------------------------------------------------------------------
# Funcion que recibe la informacion del usuario para elecicon de elminiacion


def selection(ssh_file: str, dictionary_lines: dict) -> int:
    list_main("-l",ssh_file) # Uso de funcion de lista simple de .list.py
    lenght_options = len(dictionary_lines)
    if 0 in dictionary_lines:
        lenght_options -= 1
    while True:
        selection = validator(f"\nSelect to delete [1-{lenght_options}]: ", int)
        if selection in range(1, lenght_options+1):
            break
        else:
            print(f"Error: Selected value is out of range, valid range [1-{lenght_options}]")
    print("Conection details:\n")
    for data in (dictionary_lines[selection]["lines"]):
        line = (data.replace("HostName", "ip:")
                    .replace("Host", "Name:")
                    .replace("User", "User:")
                    .replace("Port", "Port:").strip())
        print(line)
    print(" ")
    while True:
        decision = (validator("Are you sure? [Y/N]: ", str)).lower().strip()
        if decision == "y":
            return selection
        elif decision == "n":
            return 0

# -----------------------------------------------------------------------------
# Funcion que recibe todas las lineas el documento y parsea la informaicon interna


def line_parser(lines: list) -> dict:
    diccionario = {}
    bloque = 0
    for linea in lines:
        if linea.strip() == "":
            bloque += 1
            diccionario[bloque] = {
                "comments": [],
                "lines": []
            }
            continue

        if linea[0] == "#":
            if bloque == 0:
                if 0 not in diccionario:
                    diccionario[0] = [linea]
                else:
                    diccionario[0 ].append(linea)
                continue
            diccionario[bloque]["comments"].append(linea)
            continue
        if "Host" in (linea.split(' '))[0]:
            diccionario[bloque]["lines"].append(linea)
        if "    " in linea:
            diccionario[bloque]["lines"].append(linea)
    return diccionario


# -----------------------------------------------------------------------------
#  Funcion que elimina y cronstruye el nuevo texto


def delete(dictionary_lines: dict, delete_selection: int ):
    dictionary_lines.pop(delete_selection)
    new_text = []
    old_section = []

    for section in dictionary_lines:

        if not old_section:
            old_section = 0
        if old_section != section:
            old_section = section
            new_text.append("\n")
        if section == 0:
            for comment in dictionary_lines[0]:
                new_text.append(comment)
        else:
            for type_line in dictionary_lines[section]:
                for value in dictionary_lines[section][type_line]:
                    new_text.append(value)
    return "".join(new_text)



# -----------------------------------------------------------------------------
# Funcion main que ensambla todas las funfiones del modulo delete


def delete_main(ssh_file: str):
    texto = get_text(ssh_file)
    dictionary_lines = line_parser(texto)
    delete_selection = selection(ssh_file, dictionary_lines)
    new_text = delete(dictionary_lines, delete_selection)
    with open(ssh_file, "w") as archivo:
        archivo.write(new_text)
