from pasajero import Pasajero


class MiCola:
    """Cola FIFO manual de capacidad fija, ampliada con métodos de MiLista.

    En la cola normal se encola al FINAL y se desencola del FRENTE.
    Por indicación oral del profesor se añaden también las operaciones de
    la Tarea 2. Insertar, ordenar y reversar alteran el orden previo;
    después de usarlas, desencolar seguirá sacando el frente actual.

    No usar métodos integrados de list: append, insert, pop, remove, index,
    sort, reverse, copy, len(), pertenencia in, rebanadas o comprensiones.
    """

    def __init__(self, capacidad=10):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser positiva")
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    # -------------------- MÉTODOS OBLIGATORIOS DE LA GUÍA 3 --------------------

    def encolar(self, pasajero):
        if self.buscar(pasajero.numero) != -1:
            print("  ⚠ Ya existe un pasajero con ese número en la cola")
            return False
        if self.cantidad == self.capacidad:
            print("  ⚠ La cola está llena")
            return False
        self.datos[self.cantidad] = pasajero
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):
        if self.cantidad == 0:
            print("  (cola vacía)")
            return
        for i in range(self.cantidad):
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
        # Búsqueda LINEAL siempre desde el FRENTE al FINAL.
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
        # Rotar la cola completa. Solo se retira desde el frente y se
        # reinserta por el final. Se mantiene el orden relativo restante.
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
        # Copia profunda de cada pasajero: cambiar la copia no cambia el original.
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

    # --------- OPERACIONES DE MiLista (TAREA 2) PEDIDAS PARA LA COLA ---------
    # Son operaciones adicionales didácticas: algunas reorganizan la cola.

    def añadir(self, pasajero):
        """Nombre de MiLista: añadir equivale a encolar por el final."""
        return self.encolar(pasajero)

    def insertar(self, posicion, pasajero):
        """Inserta por posición moviendo manualmente a la derecha."""
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
        """Elimina por posición mediante la rotación de una vuelta completa."""
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
        """Como MiLista: buscar número y eliminar por posición encontrada."""
        posicion = self.buscar(numero)
        if posicion == -1:
            return False
        self.eliminar_por_posicion(posicion)
        return True

    def ordenar_asc(self):
        """Burbuja manual por número, de menor a mayor."""
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero > self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def ordenar_desc(self):
        """Burbuja manual por número, de mayor a menor."""
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero < self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def reversar(self):
        """Invierte el orden manualmente usando dos punteros."""
        izquierda = 0
        derecha = self.cantidad - 1
        while izquierda < derecha:
            aux = self.datos[izquierda]
            self.datos[izquierda] = self.datos[derecha]
            self.datos[derecha] = aux
            izquierda = izquierda + 1
            derecha = derecha - 1

    def esta_ordenada_asc(self):
        """Comprueba que la búsqueda binaria sea válida, sin alterar la cola."""
        for i in range(1, self.cantidad):
            if self.datos[i - 1].numero > self.datos[i].numero:
                return False
        return True

    def buscar_binaria(self, numero):
        """Búsqueda binaria manual. Solo funciona si está ordenada ascendente."""
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

    # ---- DOS MÉTODOS ADICIONALES DE ListaPython (TAREA 2) ----

    def filtrar_por_destino(self, destino):
        """Retorna una nueva MiCola con pasajeros de ese destino, en su orden.

        Se devuelve MiCola, no una lista Python, para cumplir las restricciones
        de los métodos hechos manualmente (sin append, slicing, etc.).
        """
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
        """Retorna otra MiCola con los pasajeros de 18 años o más."""
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
