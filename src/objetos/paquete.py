class Paquete:
    def __init__(self, codigo, peso, destino, cliente, estado="Pendiente"):
        self.codigo = codigo
        self.peso = float(peso)
        self.destino = destino
        self.cliente = cliente       # Instancia de Cliente
        self.estado = estado         # Pendiente, En ruta, Entregado, Cancelado