class Cliente:
    def __init__(self, id_cliente, nombre, direccion):
        self.id = id_cliente
        self.nombre = nombre
        self.direccion = direccion
        self.historial_pedidos = []  # Almacenará instancias de Paquete
