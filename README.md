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

## Limitaciones conocidas

Este proyecto tiene trade-offs técnicos que conozco y que dejé así 
a propósito, por ser un proyecto de aprendizaje y no un sistema 
en producción:

- **Montos en `float`**: los saldos, depósitos, retiros y transferencias 
  se manejan con `float` en vez de `Decimal`. Para dinero real esto es 
  un antipatrón porque el punto flotante puede acumular errores de 
  redondeo tras muchas operaciones.
- **NIP en texto plano**: el NIP se guarda como número plano en el JSON 
  y se compara directamente, sin hashing. En un sistema real las 
  credenciales nunca deberían almacenarse así.
- **Diseño a nivel de módulo**: `cajero.py` no encapsula su lógica en 
  funciones ni usa `if __name__ == "__main__":`; usa variables globales 
  sueltas (`intentos_realizados`, `bloqueo`, `usuario_encontrado`, etc.) 
  para el flujo de login en vez de pasar estado explícitamente.
- **`try/except` amplio**: algunos bloques (el menú completo en 
  `cajero.py`, el login en `cajero_interf.py`) envuelven varias 
  operaciones distintas bajo un solo `except ValueError`, lo que puede 
  ocultar errores no relacionados con el parseo de inputs.
- **Escritura de datos no atómica**: `guardar_datos()` escribe 
  directamente sobre el archivo JSON. Si el proceso se interrumpe a 
  la mitad de la escritura, el archivo puede quedar corrupto.

## Nota

Este es un proyecto educativo desarrollado por mi para aprender los fundamentos de Python: funciones, estructuras de datos, manejo de errores y construcción de interfaces gráficas con Tkinter. Los datos de usuarios, cuentas y NIPs son completamente ficticios.
