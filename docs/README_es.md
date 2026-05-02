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

* `-r` → Registrar una nueva conexión
* `-l` → Listar conexiones almacenadas
* `-e` → Editar una conexión existente
* `-d` → Eliminar una conexión

> Para más detalles, usar el sistema de ayuda integrado.

---

## 📖 Ayuda

La herramienta incluye un sistema de ayuda (`--help`) donde se detallan todas las opciones y su uso.

---

## 🛠️ Estado del proyecto

* ✅ Registro de conexiones (`-r`) implementado
* ✅ Listado de conexiones (`-l`) implementado
* ✅ Eliminación de conexiones (`-d`) implementado
* ⚙️ Edición de conexiones (`-e`) en desarrollo
* ⚙️ Comando de ayuda (`-h`) en desarrollo

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

