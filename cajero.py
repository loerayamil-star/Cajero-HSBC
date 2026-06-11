import time
import datetime

print("=== BANCO HSBC ===")

from datos import cargar_datos, guardar_datos, usuarios
usuarios = cargar_datos()

# ==========================================================================================================================
# Funciones


def fmt(monto):
    return f"${monto:,.2f}"

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

def mostrar_historial(movimientos):
    print("\n" + "="*60)
    print("         HISTORIAL DE MOVIMIENTOS")
    print("="*60)

    if not movimientos:
        print("       No hay movimientos registrados")
        return

    print(f"{'No.':<3}{'FECHA':<20}{'TIPO':<12}{'MONTO':<14}{'SALDO':<12}")
    print("-"*60)

    for i, mov in enumerate(movimientos, 1):
        signo = "+" if mov['Tipo'] == 'Depósito' else "-"
        monto_str = f"{signo}{fmt(mov['Monto'])}"
        print(f"{i:<3}{mov['fecha']:<20}{mov['Tipo']:<12}{monto_str:<14}{fmt(mov['Saldo_nuevo'])}")

def mostrar_resumen(movimientos):
    total_depositos = sum(mov['Monto'] for mov in movimientos if mov['Tipo'] == 'Depósito')
    total_retiros = sum(mov['Monto'] for mov in movimientos if mov['Tipo'] == 'Retiro')

    print("\n -RESUMEN FINANCIERO- ")
    print(f"Total de depositos: {fmt(total_depositos)}")
    print(f"Total de retiros: {fmt(total_retiros)}")
    print(f"Saldo Neto: {fmt(total_depositos - total_retiros)}")


# ==========================================================================================================================
# Validacion de usuario


intentos_realizados = 0
intentos_realizados_nip = 0
bloqueo = 0
usuario_encontrado = None

while True and usuario_encontrado is None:
    cuenta_ingresada = input("- INGRESE SU NUMERO DE CUENTA - ")

    for u in usuarios:
        if u['cuenta'] == cuenta_ingresada:
            usuario_encontrado = u
            break

    if usuario_encontrado is None:
        print("- CUENTA NO ENCONTRADA, INTENTE DE NUEVO -")
        intentos_realizados += 1

    if intentos_realizados >= 4:
        print("- Cuenta bloqueada, intente de nuevo mas tarde o llame al 55-2118-3123 -")
        bloqueo += 1
        break

if bloqueo == 1:
    exit()

while True and usuario_encontrado is not None:
    try:
        nip_ingresado = input("- INGRESE SU NIP - ")

        if usuario_encontrado['NIP'] == int(nip_ingresado):
            print("- NIP CORRECTO, ESPERE... -")
            time.sleep(5)
            break

        if nip_ingresado != usuario_encontrado['NIP']:
            print("- NIP INCORRECTO, INTENTE DE NUEVO -")
            intentos_realizados_nip += 1

        if intentos_realizados_nip >= 4:
            print("- Cuenta bloqueada, intente de nuevo mas tarde o llame al 55-2118-3123 -")
            bloqueo += 1
            break

    except ValueError:
        print("- Por favor, ingrese solo números -")

if bloqueo == 1:
    exit()


# ===========================================================================================================================
# Bienvenida


print(f"\n¡Bienvenido, {usuario_encontrado['nombre']}! Has accedido a tu cuenta con éxito.")
mostrar_resumen(usuario_encontrado['movimientos'])


# ==========================================================================================================================
# Menu de opciones


def menu(usuario):
    print("\n== Interfaz HSBC ==")
    print(f"Bienvenido, {usuario['nombre']}, ¿Que operacion deseas realizar?")
    print("1. Consultar saldo")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Historial financiero completo")
    print("5. Resumen financiero")
    print("6. Ultimos 5 movimientos")
    print("7. Soporte de cuenta")
    print("8. Salir")

    while True:
        try:
            print()
            accion = int(input("Ingrese el servicio que desea (solo numero): "))

            if accion == 1:
                print(f"Su saldo es de {fmt(usuario['saldo'])}")

            elif accion == 2:
                deposito = float(input("Ingrese el monto a depositar: $"))
                if deposito > 0:
                    saldo_anterior = usuario['saldo']
                    usuario['saldo'] += deposito
                    registrar_movimiento(usuario['movimientos'], 'Depósito', deposito, saldo_anterior, usuario['saldo'], "Deposito en efectivo")
                    print("Espere. . .")
                    time.sleep(10)
                    print(f"Depósito de {fmt(deposito)} realizado con éxito")
                    print(f"Su saldo actual es de {fmt(usuario['saldo'])}")
                    guardar_datos(usuarios)
                else:
                    print("El monto debe ser mayor a cero")

            elif accion == 3:
                retirar = float(input("Ingrese el monto a retirar: $"))
                if retirar <= 0:
                    print("El monto debe ser mayor a cero")
                elif retirar > usuario['saldo']:
                    print("Fondos insuficientes")
                else:
                    saldo_anterior = usuario['saldo']
                    usuario['saldo'] -= retirar
                    registrar_movimiento(usuario['movimientos'], 'Retiro', retirar, saldo_anterior, usuario['saldo'], "Retiro en Cajero")
                    print("Espere. . .")
                    time.sleep(10)
                    print(f"Retiro de {fmt(retirar)} realizado con éxito")
                    print(f"Su saldo actual es de {fmt(usuario['saldo'])}")
                    guardar_datos(usuarios)
            elif accion == 4:
                mostrar_historial(usuario['movimientos'])

            elif accion == 5:
                mostrar_resumen(usuario['movimientos'])

            elif accion == 6:
                print("\n -ULTIMOS 5 MOVIMIENTOS-")
                if usuario['movimientos']:
                    ultimos = usuario['movimientos'][-5:]
                    print(f"{'No.':<3}{'FECHA':<20}{'TIPO':<12}{'MONTO':<14}{'SALDO':<12}")
                    print("-"*60)
                    for i, mov in enumerate(ultimos, 1):
                        signo = "+" if mov['Tipo'] == 'Depósito' else "-"
                        monto_str = f"{signo}{fmt(mov['Monto'])}"
                        print(f"{i:<3}{mov['fecha']:<20}{mov['Tipo']:<12}{monto_str:<14}{fmt(mov['Saldo_nuevo'])}")
                else:
                    print("No hay movimientos registrados")

            elif accion == 7:
                print("Para soporte, por favor contacte a nuestro servicio al cliente al 01-800-123-4567 o envíe un correo a soporte@hsbc.com")

            elif accion == 8:
                print("¡Muchas Gracias por preferir HSBC!")
                break

            else:
                print("Opción no válida. Por favor, elija entre 1 y 8.")
                continue

            if accion != 8:
                continuar = input("\n¿Desea realizar otra operación? (s/n): ").strip().lower()
                if continuar != 's':
                    print("¡Muchas Gracias por preferir HSBC!")
                    break

        except ValueError:
            print("Error: Por favor, ingrese solo números")

menu(usuario_encontrado)


# ==========================================================================================================================
# FIN
