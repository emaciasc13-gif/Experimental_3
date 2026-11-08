from pasajero import Pasajero


class MiCola:
    """Cola (FIFO) hecha a mano sobre un arreglo de tamaño fijo.
    datos  -> [FRENTE, ..., FINAL, None, None]
    FRENTE -> datos[0]             (el primero que llegó: el único que sale)
    FINAL  -> datos[cantidad - 1]  (los nuevos se ponen detrás de él)
    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser positiva")
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0


    def encolar(self, pasajero):                     # ✅ resuelto (= añadir de MiLista)
        if self.buscar(pasajero.numero) != -1:
            print("  ⚠ Ya existe un pasajero con ese número en la cola")
            return False
        if self.cantidad == self.capacidad:
            print("  ⚠ La cola está llena")
            return False
        self.datos[self.cantidad] = pasajero          # se pone a la fila por detrás
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # ✅ EJEMPLO: del FRENTE al FINAL
        if self.cantidad == 0:
            print("  (cola vacía)")
            return
        for i in range(self.cantidad):                # 0, 1, ..., cantidad-1  (hacia adelante)
            if i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FRENTE")
            elif i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← FINAL")
            else:
                print(f"  [{i}] {self.datos[i]}")

    def desencolar(self):
        if self.cantidad == 0:
            return None
        pasajero = self.datos[0]
        for i in range(1, self.cantidad):
            self.datos[i - 1] = self.datos[i]
        self.cantidad = self.cantidad - 1
        self.datos[self.cantidad] = None
        return pasajero

    def ver_frente(self):
        if self.cantidad == 0:
            return None
        return self.datos[0]

    def buscar(self, numero):
        for i in range(self.cantidad):
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
        total_original = self.cantidad
        encontrado = False
        for i in range(total_original):
            pasajero = self.desencolar()
            if pasajero.numero == numero:
                encontrado = True
            else:
                self.encolar(pasajero)
        return encontrado

    def copiar(self):
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            original = self.datos[i]
            duplicado = Pasajero(
                original.numero, original.nombre, original.cedula,
                original.edad, original.fecha_vuelo, original.destino,
                original.asiento,
            )
            nueva.encolar(duplicado)
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0


    def añadir(self, pasajero):
        return self.encolar(pasajero)

    def insertar(self, posicion, pasajero):
        if posicion < 0 or posicion > self.cantidad:
            return False
        if self.cantidad == self.capacidad:
            return False
        if self.buscar(pasajero.numero) != -1:
            return False
        for i in range(self.cantidad, posicion, -1):
            self.datos[i] = self.datos[i - 1]
        self.datos[posicion] = pasajero
        self.cantidad = self.cantidad + 1
        return True

    def eliminar_por_posicion(self, posicion):
        if posicion < 0 or posicion >= self.cantidad:
            return None
        total_original = self.cantidad
        eliminado = None
        for i in range(total_original):
            pasajero = self.desencolar()
            if i == posicion:
                eliminado = pasajero
            else:
                self.encolar(pasajero)
        return eliminado

    def eliminar_por_valor(self, numero):
        posicion = self.buscar(numero)
        if posicion == -1:
            return False
        self.eliminar_por_posicion(posicion)
        return True

    def ordenar_asc(self):
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero > self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def ordenar_desc(self):
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero < self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def reversar(self):
        izquierda = 0
        derecha = self.cantidad - 1
        while izquierda < derecha:
            aux = self.datos[izquierda]
            self.datos[izquierda] = self.datos[derecha]
            self.datos[derecha] = aux
            izquierda = izquierda + 1
            derecha = derecha - 1

    def esta_ordenada_asc(self):
        for i in range(1, self.cantidad):
            if self.datos[i - 1].numero > self.datos[i].numero:
                return False
        return True

    def buscar_binaria(self, numero):
        if not self.esta_ordenada_asc():
            return -1
        izquierda = 0
        derecha = self.cantidad - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            actual = self.datos[medio].numero
            if actual == numero:
                return medio
            if actual < numero:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return -1


    def filtrar_por_destino(self, destino):
        resultado = MiCola(self.capacidad)
        destino_buscado = destino.strip().casefold()
        for i in range(self.cantidad):
            pasajero = self.datos[i]
            if pasajero.destino.strip().casefold() == destino_buscado:
                resultado.encolar(Pasajero(
                    pasajero.numero, pasajero.nombre, pasajero.cedula,
                    pasajero.edad, pasajero.fecha_vuelo, pasajero.destino,
                    pasajero.asiento,
                ))
        return resultado

    def mayores_de_edad(self):
        resultado = MiCola(self.capacidad)
        for i in range(self.cantidad):
            pasajero = self.datos[i]
            if pasajero.es_mayor_de_edad():
                resultado.encolar(Pasajero(
                    pasajero.numero, pasajero.nombre, pasajero.cedula,
                    pasajero.edad, pasajero.fecha_vuelo, pasajero.destino,
                    pasajero.asiento,
                ))
        return resultado
