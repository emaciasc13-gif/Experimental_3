from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola
from utils import (imprimir_exito, imprimir_error, imprimir_info,
                   leer_cedula, leer_fecha, leer_asiento, leer_texto,
                   menu, borrar_pantalla, pausar)
import utils

pila = MiPila(10)
cola = MiCola(10)


# ------------------------- funciones de apoyo ✅ -------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    return utils.leer_entero(mensaje, minimo, maximo)


def leer_pasajero():
    borrar_pantalla()
    print("\n--- INGRESO DE PASAJERO ---")
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
        op = menu("MENÚ 1 · PILA (LIFO)", [
            "Apilar pasajero", "Listar pila", "Desapilar", "Ver tope",
            "Buscar", "Modificar", "Eliminar por número", "Copiar",
            "Longitud / ¿vacía?", "Cargar datos de prueba",
        ], salida="Volver al menú principal", admitir_c=True)

        if op == "1":                                  # ✅ ejemplo resuelto
            if pila.cantidad == pila.capacidad:
                imprimir_error("La pila está llena; no se puede apilar otro pasajero.")
                pausar()
                continue
            pasajero = leer_pasajero()                 # 1. LEER
            if pila.apilar(pasajero):                  # 2. LLAMAR
                imprimir_exito("Apilado: ahora es el tope")  # 3. MOSTRAR
        elif op == "2":
            pila.listar()
        elif op == "C" or op == "10":
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
        pausar()


# ---------------------- MENÚ 2 · COLA ----------------------
def menu_cola():
    while True:
        op = menu("MENÚ 2 · COLA (FIFO)", [
            "Encolar pasajero", "Listar cola", "Desencolar", "Ver frente",
            "Buscar", "Modificar", "Eliminar por número", "Copiar",
            "Longitud / ¿vacía?", "Cargar datos de prueba",
            "[Tarea 2] Insertar en posición", "[Tarea 2] Buscar binaria",
            "[Tarea 2] Ordenar ascendente", "[Tarea 2] Ordenar descendente",
            "[Tarea 2] Reversar", "[Tarea 2] Eliminar por posición",
            "[Tarea 2] Eliminar por valor", "[Tarea 2] Filtrar por destino",
            "[Tarea 2] Mostrar mayores de edad",
        ], salida="Volver al menú principal", admitir_c=True)

        if op == "1":                                  # ✅ ejemplo resuelto
            if cola.cantidad == cola.capacidad:
                imprimir_error("La cola está llena; no se puede encolar otro pasajero.")
                pausar()
                continue
            pasajero = leer_pasajero()                 # 1. LEER
            if cola.encolar(pasajero):                 # 2. LLAMAR
                imprimir_exito("Encolado: está al final")  # 3. MOSTRAR
        elif op == "2":
            cola.listar()
        elif op == "C" or op == "10":
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
        # Operaciones adicionales de la Tarea 2, SOLO para la cola.
        # El método "añadir" corresponde a la opción 1 (encolar).
        elif op == "11":
            if cola.cantidad == cola.capacidad:
                imprimir_error("La cola está llena; no se puede insertar.")
            else:
                posicion = leer_entero("  Posición (desde 0): ", minimo=0,
                                       maximo=cola.cantidad)
                pasajero = leer_pasajero()
                if cola.insertar(posicion, pasajero):
                    imprimir_exito(f"Insertado en [{posicion}].")
                    imprimir_info("Atención: esta opción cambia el orden de llegada.")
                else:
                    imprimir_error("No se pudo insertar (número repetido, posición o capacidad).")
        elif op == "12":
            if not cola.esta_ordenada_asc():
                imprimir_error("Para búsqueda binaria, ordene primero en ascendente (opción 13).")
            else:
                numero = leer_entero("  N.º de pasajero a buscar: ", minimo=1)
                posicion = cola.buscar_binaria(numero)
                if posicion == -1:
                    imprimir_error(f"El pasajero {numero} no existe en la cola.")
                else:
                    imprimir_exito(f"Encontrado en [{posicion}]: {cola.datos[posicion]}")
        elif op == "13":
            cola.ordenar_asc()
            imprimir_exito("Cola ordenada por número, de menor a mayor.")
            imprimir_info("La operación altera el orden de llegada original.")
            cola.listar()
        elif op == "14":
            cola.ordenar_desc()
            imprimir_exito("Cola ordenada por número, de mayor a menor.")
            imprimir_info("La operación altera el orden de llegada original.")
            cola.listar()
        elif op == "15":
            cola.reversar()
            imprimir_exito("Orden de la cola invertido.")
            imprimir_info("La operación altera el orden de llegada original.")
            cola.listar()
        elif op == "16":
            if cola.esta_vacia():
                imprimir_error("La cola está vacía.")
            else:
                posicion = leer_entero("  Posición a eliminar (desde 0): ",
                                       minimo=0, maximo=cola.cantidad - 1)
                eliminado = cola.eliminar_por_posicion(posicion)
                if eliminado is None:
                    imprimir_error("No se pudo eliminar esa posición.")
                else:
                    imprimir_exito(f"Eliminado: {eliminado}")
        elif op == "17":
            numero = leer_entero("  Número de pasajero a eliminar: ", minimo=1)
            if cola.eliminar_por_valor(numero):
                imprimir_exito(f"Pasajero {numero} eliminado por valor.")
            else:
                imprimir_error(f"El pasajero {numero} no existe.")
        elif op == "18":
            destino = leer_texto("  Destino que desea filtrar: ")
            filtrados = cola.filtrar_por_destino(destino)
            imprimir_info(f"Coincidencias por destino ({destino}): {filtrados.longitud()}")
            filtrados.listar()
        elif op == "19":
            mayores = cola.mayores_de_edad()
            imprimir_info(f"Pasajeros mayores de edad: {mayores.longitud()}")
            mayores.listar()
        elif op == "0":
            break
        pausar()


# ---------------------- MENÚ PRINCIPAL ✅ ----------------------
def main():
    while True:
        op = menu("TAREA PILAS Y COLAS · PASAJEROS ✈", [
            "Menú 1 · Pila", "Menú 2 · Cola",
        ], salida="Salir del programa")
        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "0":
            imprimir_info("¡Hasta pronto!")
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma finalizado por el usuario.")
