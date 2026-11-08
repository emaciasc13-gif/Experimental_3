from pasajero import Pasajero


class MiPila:
    """Pila (LIFO) hecha a mano sobre un arreglo de tamaño fijo.
    datos -> [fondo, ..., TOPE, None, None]
    TOPE  -> datos[cantidad - 1]  (el último que entró: el único que se ve y el único que sale)
    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def apilar(self, pasajero):                      # ✅ resuelto (= añadir de MiLista)
        if self.buscar(pasajero.numero) != -1:
            print("  ⚠ Ya existe un pasajero con ese número en la pila")
            return False
        if self.cantidad == self.capacidad:
            print("  ⚠ La pila está llena")
            return False
        self.datos[self.cantidad] = pasajero          # el nuevo queda encima: es el TOPE
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # ✅ EJEMPLO: del TOPE al FONDO
        if self.cantidad == 0:
            print("  (pila vacía)")
            return
        for i in range(self.cantidad - 1, -1, -1):    # cantidad-1, ..., 1, 0  (hacia atrás)
            if i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← TOPE")
            elif i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FONDO")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------- ✅ IMPLEMENTADO (tabla 3) · búsquedas del tope al fondo -------
    def desapilar(self):
        if self.cantidad == 0:
            return None
        pasajero = self.datos[self.cantidad - 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero

    def ver_tope(self):
        if self.cantidad == 0:
            return None
        return self.datos[self.cantidad - 1]

    def buscar(self, numero):
        # La búsqueda empieza por el TOPE y termina en el FONDO.
        for i in range(self.cantidad - 1, -1, -1):
            if self.datos[i].numero == numero:
                return i
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        posicion = self.buscar(numero)
        if posicion == -1:
            return False
        self.datos[posicion].destino = nuevo_destino
        self.datos[posicion].asiento = nuevo_asiento
        return True

    def eliminar_por_numero(self, numero):
        # No se retira un elemento intermedio directamente: se usa otra pila.
        aux = MiPila(self.capacidad)
        encontrado = False
        while self.cantidad > 0:
            pasajero = self.desapilar()
            if pasajero.numero == numero:
                encontrado = True
                break
            aux.apilar(pasajero)

        # Se restauran los pasajeros que estaban sobre el eliminado.
        while aux.cantidad > 0:
            self.apilar(aux.desapilar())
        return encontrado

    def copiar(self):
        """Nueva estructura y nuevos objetos Pasajero, sin afectar el original."""
        nueva = MiPila(self.capacidad)
        # Reconstruir en orden de llegada conserva el tope o frente original.
        for i in range(self.cantidad):
            original = self.datos[i]
            duplicado = Pasajero(
                original.numero, original.nombre, original.cedula,
                original.edad, original.fecha_vuelo, original.destino,
                original.asiento,
            )
            nueva.apilar(duplicado)
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
