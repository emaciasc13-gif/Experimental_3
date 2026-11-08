from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola
from utils import (imprimir_exito, imprimir_error, imprimir_info,
                   leer_cedula, leer_fecha, leer_asiento, leer_texto)
import utils

pila = MiPila(10)
cola = MiCola(10)


# ------------------------- funciones de apoyo ✅ -------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    return utils.leer_entero(mensaje, minimo, maximo)


def leer_pasajero():
    numero = leer_entero("  N.º de pasajero: ", minimo=1)
    nombre = leer_texto("  Nombre: ", solo_letras=True)
    cedula = leer_cedula("  Cédula: ")
    edad = leer_entero("  Edad: ", minimo=0, maximo=120)
    fecha = leer_fecha("  Fecha de vuelo (AAAA-MM-DD): ")
    destino = leer_texto("  Destino: ")
    asiento = leer_asiento("  Asiento: ")
    return Pasajero(numero, nombre, cedula, edad, fecha, destino, asiento)


def datos_prueba():
    """Los 5 pasajeros de prueba en ORDEN DE LLEGADA (Diana llega primero, Elena última)."""
    return [
        Pasajero(1005, "Diana", "0923456789", 22, "2026-11-15", "Quito",  "12A"),
        Pasajero(1002, "Ana",   "0912345678", 28, "2026-11-15", "Lima",   "03C"),
        Pasajero(1009, "Luis",  "0987654321", 35, "2026-11-20", "Bogotá", "18F"),
        Pasajero(1004, "Beto",  "0934567890", 16, "2026-11-20", "Quito",  "07B"),
        Pasajero(1001, "Elena", "0901234567", 41, "2026-11-22", "Lima",   "01A"),
    ]


def mostrar_opciones(titulo, entrar, salir, ver):
    print(f"\n========== {titulo} ==========")
    print(f" 1. {entrar:<12}  2. Listar          3. {salir}")
    print(f" 4. {ver:<12}  5. Buscar          6. Modificar")
    print(" 7. Eliminar por número         8. Copiar")
    print(" 9. Longitud / ¿vacía?")
    print(" C. Cargar datos de prueba      0. Volver")


def cargar_datos_prueba(estructura, agregar):
    """Agrega los datos de ejemplo sin duplicados y explica el resultado real."""
    nuevos = 0
    repetidos = 0
    sin_espacio = 0
    for pasajero in datos_prueba():
        if estructura.buscar(pasajero.numero) != -1:
            repetidos = repetidos + 1
        elif estructura.cantidad == estructura.capacidad:
            sin_espacio = sin_espacio + 1
        elif agregar(pasajero):
            nuevos = nuevos + 1
    imprimir_info(f"Datos de prueba: {nuevos} añadidos, {repetidos} repetidos, "
                 f"{sin_espacio} sin espacio. Total: {estructura.cantidad}.")


# ---------------------- MENÚ 1 · PILA ----------------------
def menu_pila():
    while True:
        mostrar_opciones("MENÚ 1 · PILA (LIFO)", "Apilar", "Desapilar", "Ver tope")
        op = input("Opción: ").strip().upper()

        if op == "1":                                  # ✅ ejemplo resuelto
            if pila.cantidad == pila.capacidad:
                imprimir_error("La pila está llena; no se puede apilar otro pasajero.")
                continue
            pasajero = leer_pasajero()                 # 1. LEER
            if pila.apilar(pasajero):                  # 2. LLAMAR
                imprimir_exito("Apilado: ahora es el tope")  # 3. MOSTRAR
        elif op == "2":
            pila.listar()
        elif op == "C":
            cargar_datos_prueba(pila, pila.apilar)

        # ✅ Opciones 3 a 9 completas con el patrón LEER → LLAMAR → MOSTRAR
        elif op == "3":
            pasajero = pila.desapilar()
            if pasajero is None:
                imprimir_error("La pila está vacía; no hay elementos para desapilar.")
            else:
                imprimir_exito(f"Desapilado: {pasajero}")
                nuevo_tope = pila.ver_tope()
                if nuevo_tope is None:
                    imprimir_info("La pila quedó vacía.")
                else:
                    imprimir_info(f"Nuevo tope: {nuevo_tope.nombre} ({nuevo_tope.numero})")
        elif op == "4":
            pasajero = pila.ver_tope()
            if pasajero is None:
                imprimir_error("La pila está vacía.")
            else:
                imprimir_info(f"Tope: {pasajero}")
        elif op == "5":
            numero = leer_entero("  Número de pasajero a buscar: ", minimo=1)
            posicion = pila.buscar(numero)
            if posicion == -1:
                imprimir_error(f"El pasajero {numero} no existe en la pila.")
            else:
                imprimir_exito(f"Encontrado en [{posicion}]: {pila.datos[posicion]}")
        elif op == "6":
            numero = leer_entero("  Número de pasajero a modificar: ", minimo=1)
            posicion = pila.buscar(numero)
            if posicion == -1:
                imprimir_error(f"El pasajero {numero} no existe en la pila.")
            else:
                destino = leer_texto("  Nuevo destino: ")
                asiento = leer_asiento("  Nuevo asiento: ")
                if pila.modificar(numero, destino, asiento):
                    imprimir_exito(f"Modificado: {pila.datos[posicion]}")
        elif op == "7":
            numero = leer_entero("  Número de pasajero a eliminar: ", minimo=1)
            if pila.eliminar_por_numero(numero):
                imprimir_exito(f"Pasajero {numero} eliminado; se conservó el orden de la pila.")
            else:
                imprimir_error(f"El pasajero {numero} no existe en la pila.")
        elif op == "8":
            copia = pila.copiar()
            imprimir_info("Copia de la pila (tope y fondo conservados):")
            copia.listar()
            imprimir_info(f"Original: {pila.longitud()} | Copia: {copia.longitud()}")
        elif op == "9":
            imprimir_info(f"Longitud: {pila.longitud()} | "
                         f"¿Está vacía?: {'Sí' if pila.esta_vacia() else 'No'}")
        elif op == "0":
            break
        else:
            imprimir_error("Opción no válida.")


# ---------------------- MENÚ 2 · COLA ----------------------
def menu_cola():
    while True:
        mostrar_opciones("MENÚ 2 · COLA (FIFO)", "Encolar", "Desencolar", "Ver frente")
        op = input("Opción: ").strip().upper()

        if op == "1":                                  # ✅ ejemplo resuelto
            if cola.cantidad == cola.capacidad:
                imprimir_error("La cola está llena; no se puede encolar otro pasajero.")
                continue
            pasajero = leer_pasajero()                 # 1. LEER
            if cola.encolar(pasajero):                 # 2. LLAMAR
                imprimir_exito("Encolado: está al final")  # 3. MOSTRAR
        elif op == "2":
            cola.listar()
        elif op == "C":
            cargar_datos_prueba(cola, cola.encolar)

        # ✅ Opciones 3 a 9 completas con el patrón LEER → LLAMAR → MOSTRAR
        elif op == "3":
            pasajero = cola.desencolar()
            if pasajero is None:
                imprimir_error("La cola está vacía; no hay elementos para desencolar.")
            else:
                imprimir_exito(f"Desencolado: {pasajero}")
                nuevo_frente = cola.ver_frente()
                if nuevo_frente is None:
                    imprimir_info("La cola quedó vacía.")
                else:
                    imprimir_info(f"Nuevo frente: {nuevo_frente.nombre} ({nuevo_frente.numero})")
        elif op == "4":
            pasajero = cola.ver_frente()
            if pasajero is None:
                imprimir_error("La cola está vacía.")
            else:
                imprimir_info(f"Frente: {pasajero}")
        elif op == "5":
            numero = leer_entero("  Número de pasajero a buscar: ", minimo=1)
            posicion = cola.buscar(numero)
            if posicion == -1:
                imprimir_error(f"El pasajero {numero} no existe en la cola.")
            else:
                imprimir_exito(f"Encontrado en [{posicion}]: {cola.datos[posicion]}")
        elif op == "6":
            numero = leer_entero("  Número de pasajero a modificar: ", minimo=1)
            posicion = cola.buscar(numero)
            if posicion == -1:
                imprimir_error(f"El pasajero {numero} no existe en la cola.")
            else:
                destino = leer_texto("  Nuevo destino: ")
                asiento = leer_asiento("  Nuevo asiento: ")
                if cola.modificar(numero, destino, asiento):
                    imprimir_exito(f"Modificado: {cola.datos[posicion]}")
        elif op == "7":
            numero = leer_entero("  Número de pasajero a eliminar: ", minimo=1)
            if cola.eliminar_por_numero(numero):
                imprimir_exito(f"Pasajero {numero} eliminado; se conservó el orden de la cola.")
            else:
                imprimir_error(f"El pasajero {numero} no existe en la cola.")
        elif op == "8":
            copia = cola.copiar()
            imprimir_info("Copia de la cola (frente y final conservados):")
            copia.listar()
            imprimir_info(f"Original: {cola.longitud()} | Copia: {copia.longitud()}")
        elif op == "9":
            imprimir_info(f"Longitud: {cola.longitud()} | "
                         f"¿Está vacía?: {'Sí' if cola.esta_vacia() else 'No'}")
        elif op == "0":
            break
        else:
            imprimir_error("Opción no válida.")


# ---------------------- MENÚ PRINCIPAL ✅ ----------------------
def main():
    while True:
        print("\n===== TAREA PILAS Y COLAS · PASAJEROS ✈ =====")
        print("1. Menú 1 · Pila")
        print("2. Menú 2 · Cola")
        print("3. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado por el usuario.")
