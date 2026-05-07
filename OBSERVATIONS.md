# Observaciones - Validaciones y Manejo de Errores Faltantes

## `commands/register.py`

### `parseo_de_direccion()`
- No valida si el argumento es `None` o string vacío antes de procesar
- No valida que `port` sea un número válido (acepta "99999" sin verificar rango)
- No valida que `hostname` sea una IP válida o un hostname válido
- No valida que `user` no esté vacío

### `name_exist()`
- No maneja el caso donde el archivo SSH config no existe → crashea con `FileNotFoundError`
- No maneja permisos de lectura denegados

### `agregar_alias()`
- No maneja el caso donde el archivo no tiene permisos de lectura
- El `validator()` no valida que el alias no contenga caracteres inválidos para SSH (espacios, caracteres especiales)

### `agregar_conexion()` y `register_main()`
- No valida si el archivo config existe antes de intentar abrirlo en modo append
- No maneja `PermissionError` si el archivo es solo lectura
- No maneja error de disco lleno al escribir
- No hace backup del archivo antes de modificarlo
- No valida que el directorio padre exista (`~/.ssh/` podría no existir)

---

## `commands/list.py`

### `get_text()` y `get_conections()`
- No maneja archivo inexistente → crashea con `FileNotFoundError`
- No maneja permisos denegados
- No valida que el archivo tenga contenido (lista vacía sin mensaje claro al usuario)

### `list_main()`
- No valida que el archivo pasado sea realmente un archivo SSH config válido

---

## `commands/delete.py`

### `get_text()`
- No maneja archivo inexistente
- No maneja permisos denegados

### `line_parser()`
- No valida que el contenido del archivo tenga bloques Host válidos
- Si el archivo está corrupto o mal formado, puede generar un diccionario inconsistente

### `delete_main()`
- **Riesgo crítico:** No hace backup del archivo antes de sobrescribirlo
- No maneja error de disco lleno al escribir
- No maneja `PermissionError` en escritura
- Si el proceso se interrumpe a mitad de escritura, el archivo queda corrupto/truncado

---

## `core/orchestrator.py`

### `config_file()`
- Asume que al menos uno de los dos paths existe siempre
- No maneja el caso donde ambos archivos de config INI no existen
- No valida que el archivo INI sea parseable correctamente

### `obtener_argumentos()`
- `"directorio_ssh"`: si ningún directorio configurado contiene el archivo config, retorna `None` sin avisar
- No valida que los paths en `config.ini` sean válidos o existan

### `ejecutar_funcion()`
- No maneja excepciones lanzadas por las funciones de comando
- Si un comando falla, no hay catch general → traceback crudo al usuario

---

## `core/cli.py`

### `validar_flag()`
- Anotación de tipo incorrecta: dice `-> bool` pero retorna `str` o `False`
- No maneja `IndexError` si `sys.argv` está vacío (aunque ya tiene check previo)

### `validar_cantidad()`
- Solo verifica cantidad, no validez del contenido de los argumentos

### `main()`
- Único try/except es para `KeyboardInterrupt`
- No hay catch general para excepciones inesperadas → traceback crudo

---

## `core/internal/validation.py`

### `validator()`
- No maneja `EOFError` (Ctrl+D en input) → crashea
- No tiene límite de reintentos (loop infinito si el usuario nunca ingresa valor válido)

---

## `assistant/error/error_handler.py`

### Clase `Error`
- **Bug:** `Error("ER001").print()` se ejecuta al hacer import — código debug no debería ejecutarse al importar
- `errors.json` no existe en el repo → `FileNotFoundError` garantizado
- Path relativo `"errors.json"` → solo funciona si el CWD es el directorio correcto
- `print(self.error)` espera que la key exista en el JSON, si no → `KeyError`
- Este módulo no está integrado en ningún comando actualmente

---

## General

### I/O de archivos (todos los módulos)
- Ningún módulo maneja:
  - `FileNotFoundError` (archivo no existe)
  - `PermissionError` (permisos denegados)
  - `IsADirectoryError` (path es directorio en vez de archivo)
  - Disk full al escribir
  - Archivos corruptos o mal formados

### Operaciones destructivas
- `register.py` y `delete.py` modifican `~/.ssh/config` sin:
  - Crear backup previo
  - Verificar integridad después de escribir
  - Modo dry-run o confirmación explícita (en register)

### Validación de paths
- No se sanitizan paths del usuario en `config.ini`
- No se valida que los directorios existan antes de usarlos
