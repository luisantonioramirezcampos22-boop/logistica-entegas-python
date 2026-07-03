import csv
import os
from objetos.cliente import Cliente
from objetos.paquete import Paquete
from objetos.repartidor import Repartidor

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

def cargar_desde_csv():
    clientes = {}
    paquetes = {}
    repartidores = {}
    
    # 1. Clientes
    path_c = os.path.join(DATA_DIR, 'clientes.csv')
    if os.path.exists(path_c):
        with open(path_c, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row: clientes[row[0]] = Cliente(row[0], row[1], row[2])
                    
    # 2. Paquetes
    path_p = os.path.join(DATA_DIR, 'paquetes.csv')
    if os.path.exists(path_p):
        with open(path_p, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row:
                    codigo, peso, destino, c_id, estado = row
                    cliente_instancia = clientes.get(c_id)
                    if cliente_instancia:
                        np = Paquete(codigo, peso, destino, cliente_instancia, estado)
                        paquetes[codigo] = np
                        cliente_instancia.historial_pedidos.append(np)

    # 3. Repartidores
    path_r = os.path.join(DATA_DIR, 'repartidores.csv')
    if os.path.exists(path_r):
        with open(path_r, 'r', encoding='utf-8') as f:
            for row in csv.reader(f):
                if row:
                    nombre, vehiculo, zona, codigos_str = row
                    rep = Repartidor(nombre, vehiculo, zona)
                    if codigos_str:
                        for cod in codigos_str.split(";"):
                            paq = paquetes.get(cod)
                            if paq: rep.paquetes_asignados.append(paq)
                    repartidores[nombre] = rep
                    
    return clientes, paquetes, repartidores

def guardar_a_csv(clientes, paquetes, repartidores):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(os.path.join(DATA_DIR, 'clientes.csv'), 'w', newline='', encoding='utf-8') as f:
        for c in clientes.values(): csv.writer(f).writerow([c.id, c.nombre, c.direccion])
            
    with open(os.path.join(DATA_DIR, 'paquetes.csv'), 'w', newline='', encoding='utf-8') as f:
        for p in paquetes.values(): csv.writer(f).writerow([p.codigo, p.peso, p.destino, p.cliente.id, p.estado])
            
    with open(os.path.join(DATA_DIR, 'repartidores.csv'), 'w', newline='', encoding='utf-8') as f:
        for r in repartidores.values():
            cods = ";".join([p.codigo for p in r.paquetes_asignados])
            csv.writer(f).writerow([r.nombre, r.vehiculo, r.zona_actual, cods])
