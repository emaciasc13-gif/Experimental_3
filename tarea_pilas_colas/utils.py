
from datetime import datetime
import os
import re
import sys


def colorear(mensaje, codigo):
    admite_ansi = sys.stdout.isatty() and (
        os.name != "nt" or os.environ.get("WT_SESSION") or os.environ.get("ANSICON")
    )
    if admite_ansi and not os.environ.get("NO_COLOR"):
        return f"\033[{codigo}m{mensaje}\033[0m"
    return mensaje


def imprimir_exito(mensaje):
    print("  " + colorear("✓ " + mensaje, "32"))


def imprimir_error(mensaje):
    print("  " + colorear("⚠ " + mensaje, "31"))


def imprimir_info(mensaje):
    print("  " + colorear("ℹ " + mensaje, "36"))


def leer_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            numero = int(input(mensaje).strip())
        except ValueError:
            imprimir_error("Debe ingresar un número entero válido.")
            continue
        if minimo is not None and numero < minimo:
            imprimir_error(f"El valor debe ser mayor o igual que {minimo}.")
            continue
        if maximo is not None and numero > maximo:
            imprimir_error(f"El valor debe ser menor o igual que {maximo}.")
            continue
        return numero


def leer_texto(mensaje, maximo=80, solo_letras=False):
    while True:
        texto = " ".join(input(mensaje).strip().split())
        if not texto:
            imprimir_error("Este campo no puede quedar vacío.")
            continue
        if len(texto) > maximo:
            imprimir_error(f"Se permiten como máximo {maximo} caracteres.")
            continue
        if solo_letras:
            correcto = True
            for caracter in texto:
                if not (caracter.isalpha() or caracter == " " or caracter == "-" or caracter == "'"):
                    correcto = False
                    break
            if not correcto:
                imprimir_error("Use solamente letras, espacios, guiones o apóstrofos.")
                continue
        return texto


def leer_cedula(mensaje):
    while True:
        cedula = input(mensaje).strip()
        if re.fullmatch(r"[0-9]{10}", cedula):
            return cedula
        imprimir_error("La cédula debe tener exactamente 10 dígitos numéricos.")


def leer_fecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fecha):
            imprimir_error("Formato incorrecto. Escriba la fecha como AAAA-MM-DD.")
            continue
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            imprimir_error("La fecha no existe en el calendario.")
            continue
        return fecha


def leer_asiento(mensaje):
    while True:
        asiento = input(mensaje).strip().upper()
        if re.fullmatch(r"[0-9]{1,3}[A-Z]", asiento) and int(asiento[:-1]) > 0:
            return asiento
        imprimir_error("Asiento inválido. Use fila y letra, por ejemplo 12A o 03C.")


def borrar_pantalla():
    if sys.stdout.isatty():
        if os.name == "nt":
            os.system("cls")
        else:
            print("\033[2J\033[H", end="")


def pausar():
    if sys.stdin.isatty():
        try:
            input("\n  Presione Enter para continuar...")
        except EOFError:
            pass


def menu(titulo, opciones, salida="Volver", admitir_c=False):
    while True:
        borrar_pantalla()
        print(f"\n{'=' * 14} {titulo} {'=' * 14}")
        for i in range(len(opciones)):
            print(f" {i + 1:>2}. {opciones[i]}")
        print(f"  0. {salida}")
        opcion = input("\nElija una opción: ").strip().upper()
        if opcion == "0" or (admitir_c and opcion == "C"):
            return opcion
        if opcion.isdigit() and 1 <= int(opcion) <= len(opciones):
            return str(int(opcion))
        imprimir_error("Opción no válida. Elija una de las opciones del menú.")
        pausar()
