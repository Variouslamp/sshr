# 🔐 SSHR

**SSHR (SSH Register)** es una herramienta en Python diseñada para facilitar el manejo de conexiones SSH mediante alias, permitiendo registrar, editar y eliminar configuraciones sin modificar manualmente el archivo `~/.ssh/config`.

---

## 🚀 ¿Qué es SSHR?

SSHR automatiza la creación y gestión de entradas SSH, permitiendo trabajar de forma más cómoda con múltiples conexiones.

---

## ⚙️ ¿Cómo funciona?

SSHR procesa una dirección en formato:

```bash
usuario@host:puerto
```

Y genera automáticamente una entrada en el archivo SSH:

```bash
Host mi-servidor
    HostName 192.168.1.1
    User user
    Port 22
```

---

## 🏁 Funcionalidades principales

SSHR funciona mediante flags:

| Flag | Comando | Descripción |
|------|---------|-------------|
| `-r`, `--register` | register | Registrar una nueva conexión |
| `-l` | list | Listar conexiones (compacto) |
| `-ll` | list | Listar conexiones (detallado) |
| `-d`, `--delete` | delete | Eliminar una conexión (interactivo) |
| `-e`, `--edit` | edit | Editar una conexión (en desarrollo) |
| `--build` | build | Construir estructura de directorios (en desarrollo) |
| `-h`, `--help [tema]` | help | Mostrar ayuda general, de un comando o de un error |

---

## 📖 Ayuda

La herramienta incluye un sistema de ayuda integrado con tres modos:

```bash
sshr -h                  # Ayuda general — muestra todos los comandos
sshr -h register         # Ayuda de un comando — muestra uso y ejemplos
sshr -h ERR012           # Ayuda de error — explica qué significa el error
```

---

## 🔧 Primer uso

Después de instalar SSHR, ejecuta primero `sshr --build`. Esto prepara los archivos y directorios necesarios para que SSHR funcione correctamente: copia los archivos de configuración de SSHR en `~/.config/sshr`, crea `~/.ssh` si hace falta y asegura que exista `~/.ssh/config` antes de empezar a usar la herramienta.

---

## 🛠️ Estado del proyecto

* ✅ Registro de conexiones (`-r`) implementado
* ✅ Listado de conexiones (`-l`) implementado
* ✅ Eliminación de conexiones (`-d`) implementado
* ⚙️ Edición de conexiones (`-e`) en desarrollo
* ✅ Comando de ayuda (`-h`) implementado

---

## 💻 Compatibilidad

SSHR esta siendo desarrollado y probado en sistemas GNU/Linux.

El soporte para windows no se encuentra implementados y se planea para desarrollo futuro.

---

## 🧠 Filosofía del proyecto

* Mantener simplicidad y claridad
* Automatizar tareas repetitivas
* Evitar sobrevalidación innecesaria
* Dar control al usuario

---

## 📌 Notas

* SSHR no reemplaza SSH, lo complementa
* Está pensado como una herramienta ligera y práctica
* Ideal para uso personal y aprendizaje
