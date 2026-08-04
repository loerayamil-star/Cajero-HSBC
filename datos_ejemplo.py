import json


def guardar_datos(usuarios):
    with open("datos_ejemplo.json", "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def cargar_datos():
    try:
        with open("datos_ejemplo.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        from datos_ejemplo import usuarios
        return usuarios

usuarios = [
    {'nombre': 'Usuario1', 'cuenta': '000000001', 'NIP': 1234, 'saldo': 10000, 'movimientos': []},
    {'nombre': 'Usuario2', 'cuenta': '000000002', 'NIP': 5678, 'saldo': 10000, 'movimientos': []},
    {'nombre': 'Usuario3', 'cuenta': '000000003', 'NIP': 1111, 'saldo': 10000, 'movimientos': []},
    {'nombre': 'Usuario4', 'cuenta': '000000004', 'NIP': 2222, 'saldo': 10000, 'movimientos': []},
]
