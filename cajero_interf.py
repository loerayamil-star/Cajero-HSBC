import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import datetime


# === Datos =====================================================================


from datos import usuarios


def fmt(monto):
    return f"${monto:,.2f}"


# === Ventana principal =========================================================


ventana = tk.Tk()
ventana.title("Banco HSBC")
ventana.geometry("400x580")


# === Frame de Login ============================================================


frame_login = tk.Frame(ventana)
frame_login.pack(pady=20)

tk.Label(frame_login, text="=== BANCO HSBC ===", font=("Arial", 16)).pack(pady=10)
tk.Label(frame_login, text="Número de cuenta:").pack()
entrada_cuenta = tk.Entry(frame_login)
entrada_cuenta.pack(pady=5)
tk.Label(frame_login, text="NIP:").pack()
entrada_nip = tk.Entry(frame_login, show="*")
entrada_nip.pack(pady=5)


# === Validar Usuario ===========================================================


usuario_activo = None
intentos_login = 0

def validar_login():
    global usuario_activo, intentos_login

    try:
        usuario_encontrado = None
        for u in usuarios:
            if u['cuenta'] == entrada_cuenta.get():
                usuario_encontrado = u
                break

        if usuario_encontrado is None:
            intentos_login += 1
            if intentos_login >= 3:
                messagebox.showerror("Bloqueado", "Demasiados intentos fallidos. La aplicación se cerrará.")
                ventana.destroy()
                return
            messagebox.showerror("Error", f"Número de cuenta no encontrado. Intento {intentos_login}/3.")
            return

        if usuario_encontrado['NIP'] != int(entrada_nip.get()):
            intentos_login += 1
            if intentos_login >= 3:
                messagebox.showerror("Bloqueado", "Demasiados intentos fallidos. La aplicación se cerrará.")
                ventana.destroy()
                return
            messagebox.showerror("Error", f"NIP incorrecto. Intento {intentos_login}/3.")
            return

        intentos_login = 0
        usuario_activo = usuario_encontrado
        nombre_usuario.set(f"Bienvenido, {usuario_encontrado['nombre']}")
        frame_login.pack_forget()
        frame_menu.pack()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

tk.Button(frame_login, text="Ingresar", command=validar_login).pack(pady=10)


# === Frame de Menu ============================================================


frame_menu = tk.Frame(ventana)
nombre_usuario = tk.StringVar()
tk.Label(frame_menu, textvariable=nombre_usuario, font=("Arial", 14)).pack(pady=10)


def registrar_movimiento(movimientos, Tipo, Monto, Saldo_anterior, Saldo_nuevo, descripcion=""):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    movimiento = {
        'fecha': fecha,
        'Tipo': Tipo,
        'Monto': Monto,
        'Saldo_anterior': Saldo_anterior,
        'Saldo_nuevo': Saldo_nuevo,
        'descripcion': descripcion
    }
    movimientos.append(movimiento)


def consultar_saldo():
    messagebox.showinfo("Saldo", f"Su saldo es: {fmt(usuario_activo['saldo'])}")


def retirar_dinero():
    monto = simpledialog.askfloat("Retiro", "Ingrese el monto a retirar:")
    if monto is None:
        return
    if monto <= 0:
        messagebox.showerror("Error", "Por favor, ingrese un monto válido.")
    elif monto > usuario_activo['saldo']:
        messagebox.showerror("Error", "Fondos insuficientes.")
    else:
        saldo_anterior = usuario_activo['saldo']
        usuario_activo['saldo'] -= monto
        registrar_movimiento(usuario_activo['movimientos'], "Retiro", monto, saldo_anterior, usuario_activo['saldo'])
        messagebox.showinfo("Retiro", f"Se ha retirado {fmt(monto)}.\nSu nuevo saldo es: {fmt(usuario_activo['saldo'])}")


def depositar_dinero():
    monto = simpledialog.askfloat("Depósito", "Ingrese el monto a depositar:")
    if monto is None:
        return
    if monto <= 0:
        messagebox.showerror("Error", "Por favor, ingrese un monto válido.")
    else:
        saldo_anterior = usuario_activo['saldo']
        usuario_activo['saldo'] += monto
        registrar_movimiento(usuario_activo['movimientos'], "Depósito", monto, saldo_anterior, usuario_activo['saldo'])
        messagebox.showinfo("Depósito", f"Se ha depositado {fmt(monto)}.\nSu nuevo saldo es: {fmt(usuario_activo['saldo'])}")


def transferir_dinero():
    cuenta_destino = simpledialog.askstring("Transferencia", "Ingrese el número de cuenta destino:")
    if cuenta_destino is None:
        return

    usuario_destino = None
    for u in usuarios:
        if u['cuenta'] == cuenta_destino:
            usuario_destino = u
            break

    if usuario_destino is None:
        messagebox.showerror("Error", "Número de cuenta no encontrado.")
        return

    if usuario_destino['cuenta'] == usuario_activo['cuenta']:
        messagebox.showerror("Error", "No puede transferir a su propia cuenta.")
        return

    monto = simpledialog.askfloat("Transferencia", f"Ingrese el monto a transferir a {usuario_destino['nombre']}:")
    if monto is None:
        return
    elif monto <= 0:
        messagebox.showerror("Error", "Por favor, ingrese un monto válido.")
        return
    elif monto > usuario_activo['saldo']:
        messagebox.showerror("Error", "Fondos insuficientes.")
        return

    saldo_anterior_origen = usuario_activo['saldo']
    saldo_anterior_destino = usuario_destino['saldo']

    usuario_activo['saldo'] -= monto
    usuario_destino['saldo'] += monto

    registrar_movimiento(usuario_activo['movimientos'], "Transferencia enviada", monto, saldo_anterior_origen, usuario_activo['saldo'], f"A {usuario_destino['nombre']}")
    registrar_movimiento(usuario_destino['movimientos'], "Transferencia recibida", monto, saldo_anterior_destino, usuario_destino['saldo'], f"De {usuario_activo['nombre']}")

    messagebox.showinfo("Transferencia", f"Se han transferido {fmt(monto)} a {usuario_destino['nombre']}.\nSu nuevo saldo es: {fmt(usuario_activo['saldo'])}")


def historial_financiero():
    if usuario_activo['movimientos']:
        historial = "\n".join([f"{m['fecha']} - {m['Tipo']} - {fmt(m['Monto'])} - Saldo: {fmt(m['Saldo_nuevo'])}" for m in usuario_activo['movimientos']])
        messagebox.showinfo("Historial Financiero", historial)
    else:
        messagebox.showinfo("Historial Financiero", "No hay movimientos registrados.")


def resumen_financiero():
    total_depositos = sum(mov['Monto'] for mov in usuario_activo['movimientos'] if mov['Tipo'] == 'Depósito')
    total_retiros = sum(mov['Monto'] for mov in usuario_activo['movimientos'] if mov['Tipo'] == 'Retiro')
    total_transferencias = sum(mov['Monto'] for mov in usuario_activo['movimientos'] if mov['Tipo'] == 'Transferencia enviada')
    saldo_neto = total_depositos - total_retiros - total_transferencias
    resumen = (
        f"Total de depósitos: {fmt(total_depositos)}\n"
        f"Total de retiros: {fmt(total_retiros)}\n"
        f"Total de transferencias enviadas: {fmt(total_transferencias)}\n"
        f"Saldo Neto: {fmt(saldo_neto)}"
    )
    messagebox.showinfo("Resumen Financiero", resumen)


def ultimos_movimientos():
    ultimos = usuario_activo['movimientos'][-5:]
    if ultimos:
        historial = "\n".join([f"{m['fecha']} - {m['Tipo']} - {fmt(m['Monto'])} - Saldo: {fmt(m['Saldo_nuevo'])}" for m in ultimos])
        messagebox.showinfo("Últimos 5 Movimientos", historial)
    else:
        messagebox.showinfo("Últimos 5 Movimientos", "No hay movimientos registrados.")


def cambiar_nip():
    nip_actual = simpledialog.askinteger("Cambiar NIP", "Ingrese su NIP actual:")
    if nip_actual is None:
        return
    if nip_actual != usuario_activo['NIP']:
        messagebox.showerror("Error", "NIP incorrecto.")
        return

    nip_nuevo = simpledialog.askinteger("Cambiar NIP", "Ingrese su nuevo NIP:")
    if nip_nuevo is None:
        return

    nip_confirmacion = simpledialog.askinteger("Cambiar NIP", "Confirme su nuevo NIP:")
    if nip_confirmacion is None:
        return

    if nip_nuevo != nip_confirmacion:
        messagebox.showerror("Error", "Los NIPs no coinciden.")
        return

    usuario_activo['NIP'] = nip_nuevo
    messagebox.showinfo("NIP actualizado", "Su NIP ha sido actualizado correctamente.")


def soporte():
    messagebox.showinfo("Soporte", "Para soporte, contacte a nuestro servicio al cliente al 01-800-123-4567\no envíe un correo a soporte@hsbc.com")


def cerrar_sesion():
    global usuario_activo, intentos_login
    usuario_activo = None
    intentos_login = 0
    entrada_cuenta.delete(0, tk.END)
    entrada_nip.delete(0, tk.END)
    frame_menu.pack_forget()
    frame_login.pack(pady=20)


def salir():
    ventana.destroy()


tk.Button(frame_menu, text="1. Consultar saldo",       command=consultar_saldo).pack(pady=2)
tk.Button(frame_menu, text="2. Retirar dinero",        command=retirar_dinero).pack(pady=2)
tk.Button(frame_menu, text="3. Depositar dinero",      command=depositar_dinero).pack(pady=2)
tk.Button(frame_menu, text="4. Transferir dinero",     command=transferir_dinero).pack(pady=2)
tk.Button(frame_menu, text="5. Historial financiero",  command=historial_financiero).pack(pady=2)
tk.Button(frame_menu, text="6. Resumen Financiero",    command=resumen_financiero).pack(pady=2)
tk.Button(frame_menu, text="7. Últimos 5 movimientos", command=ultimos_movimientos).pack(pady=2)
tk.Button(frame_menu, text="8. Cambiar NIP",           command=cambiar_nip).pack(pady=2)
tk.Button(frame_menu, text="9. Soporte",               command=soporte).pack(pady=2)
tk.Button(frame_menu, text="10. Cerrar sesión",        command=cerrar_sesion).pack(pady=2)
tk.Button(frame_menu, text="11. Salir",                command=salir).pack(pady=5)


# === Arrancar la aplicación ====================================================


ventana.mainloop()
