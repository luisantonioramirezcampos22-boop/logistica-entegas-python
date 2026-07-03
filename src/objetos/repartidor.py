class Repartidor:
    def __init__(self, nombre, vehiculo, zona_actual):
        self.nombre = nombre
        self.vehiculo = vehiculo
        self.zona_actual = zona_actual
        self.paquetes_asignados = [] # Almacenará instancias de Paquete