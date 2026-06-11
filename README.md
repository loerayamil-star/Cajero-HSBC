# Cajero Automático HSBC — Proyecto Educativo

Simulador de cajero automático desarrollado en Python como proyecto de aprendizaje. Incluye dos versiones: una de terminal y una con interfaz gráfica.

---

## Funcionalidades

- **Login con bloqueo**: validación de número de cuenta y NIP, con bloqueo automático tras 3 intentos fallidos
- **Consultar saldo**: muestra el saldo disponible de la cuenta
- **Depositar dinero**: ingresa un monto y actualiza el saldo
- **Retirar dinero**: valida fondos suficientes antes de proceder
- **Transferir dinero**: envía dinero a otra cuenta registrada en el sistema
- **Historial financiero**: muestra todos los movimientos con fecha, tipo y saldo resultante
- **Resumen financiero**: totales de depósitos, retiros y transferencias enviadas
- **Últimos 5 movimientos**: vista rápida de la actividad reciente
- **Cambiar NIP**: permite actualizar el NIP con verificación del actual *(solo versión gráfica)*
- **Cerrar sesión**: regresa al login sin cerrar la aplicación *(solo versión gráfica)*

---

## Cómo ejecutar

### Versión terminal

```bash
python cajero.py
```

### Versión con interfaz gráfica

```bash
python cajero_interf.py
```

> **Nota:** Para ejecutar cualquiera de las dos versiones necesitas tener el archivo `datos.py` en la misma carpeta. Este archivo no se incluye en el repositorio. Puedes usar `datos_ejemplo.py` como referencia para crear el tuyo: cópialo, renómbralo a `datos.py` y ajusta los datos.

---

## Tecnologías

- Python 3
- Tkinter (interfaz gráfica)
- datetime (registro de movimientos con fecha y hora)

---

## 🔒 Seguridad

Los datos de usuarios (NIPs y cuentas) se almacenan en `datos.py` 
y `datos.json` que están en `.gitignore` para evitar exponer 
información sensible en el repositorio.

Usa `datos_ejemplo.py` y `datos_ejemplo.json` como referencia 
para crear tus propios archivos de datos locales.

Este proyecto fue mi primer contacto con buenas prácticas 
de seguridad en código — detecté que `datos.json` podía 
exponer información y lo resolví antes de subir los cambios.

## Nota

Este es un proyecto educativo desarrollado por mi para aprender los fundamentos de Python: funciones, estructuras de datos, manejo de errores y construcción de interfaces gráficas con Tkinter. Los datos de usuarios, cuentas y NIPs son completamente ficticios.
