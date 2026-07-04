import sys
import os

# Aqui permite ajustar rutas de importación de Python para reconocer carpetas internas
sys.path.append(os.path.dirname(__file__))

from src.modules.leerCSV import cargar_desde_csv, guardar_a_csv
from src.modules.leerJSON import cargar_grafo_json
from src.objetos.cliente import Cliente
from src.objetos.paquete import Paquete
from src.objetos.repartidor import Repartidor
from src.objetos.rutas import CiudadGrafo

def ordenar_paquetes_por_peso(lista):
    """Ordena colecciones de paquetes de mayor a menor peso."""
    return sorted(lista, key=lambda p: p.peso, reverse=True)

def main():
    # Carga automática de persistencia al abrir el programa
    clientes, paquetes, repartidores = cargar_desde_csv()
    datos_grafo = cargar_grafo_json()
    ciudad = CiudadGrafo(datos_grafo)
    
    while True:
        print("\nLogística De Entregas Inteligente")
        print("1. Registrar nuevo Cliente")
        print("2. Registrar nuevo Paquete")
        print("3. Registrar nuevo Repartidor")
        print("4. Mostrar Inventario General")
        print("5. Actualizar Estado de un Paquete (CRUD)")
        print("6. Calcular Ruta de Despacho (DFS)")
        print("7. Reporte de Repartidor (Ordenado por Peso)")
        print("8. Guardar y Salir")
        
        op = input("Seleccione una opción: ").strip()
        
        if op == "1":
            print("\nRegistrar cliente")
            id_c = input("ID único del cliente: ").strip()
            if id_c in clientes:
                print("Error: Ese ID ya se encuentra registrado.")
                continue
            nombre = input("Nombre completo: ").strip()
            direccion = input("Dirección de entrega: ").strip()
            
            # Guardado en el diccionario en memoria
            clientes[id_c] = Cliente(id_c, nombre, direccion)
            print(f"Cliente '{nombre}' registrado.")
        
        elif op == "2":
            print("\nRegistrar Paquete")
            if not clientes:
                print("No hay clientes en el sistema. Registre uno primero.")
                continue
                
            codigo = input("Código de paquete: ").strip()
            if codigo in paquetes:
                print("Error: Este código de paquete ya existe.")
                continue
                
            peso = input("Peso del paquete (kg): ").strip()
            destino = input("Zona destino (Centro, Norte, Sur, Este, Oeste): ").strip() 
            
            if destino not in ciudad.grafo:
                print(f"Error: La zona '{destino}' no existe en el mapa vial (rutas.json).")
                continue
            
            id_cliente = input("ID del cliente dueño del paquete: ").strip()
            
            cliente_asociado = clientes.get(id_cliente)
            if cliente_asociado:
                nuevo_p = Paquete(codigo, peso, destino, cliente_asociado)
                paquetes[codigo] = nuevo_p
                cliente_asociado.historial_pedidos.append(nuevo_p)
                print(f"paquete '{codigo}' registrado y asignado a {cliente_asociado.nombre}.")
            else:
                print("Error: El ID de cliente ingresado no existe.")
                
        elif op == "3":
            print("\nRegistrar Reparridor")
            nombre = input("Nombre del repartidor: ").strip()
            if nombre in repartidores:
                print("Error: Ya existe un repartidor con ese nombre.")
                continue
            vehiculo = input("Vehículo (Moto / Camión / Auto): ").strip()
            zona = input("Zona inicial de operación: ").strip()
            
            repartidores[nombre] = Repartidor(nombre, vehiculo, zona)
            print(f"Repartidor '{nombre}' dado de alta en la flotilla.")
            
        elif op == "4":
            print("\nInventario General De Paquetes")
            if not paquetes:
                print("No hay paquetes registrados en el sistema.")
            for p in paquetes.values():
                print(f"Código: {p.codigo} | Peso: {p.peso}kg | Destino: {p.destino} | Estado: {p.state if hasattr(p, 'state') else p.estado} | Cliente: {p.cliente.nombre}")
                
        elif op == "5":
            print("\nActualizar Estado De Paquete")
            codigo = input("Ingrese el código del paquete: ").strip()
            p = paquetes.get(codigo)
            if p:
                print(f"Estado actual del paquete: '{p.estado}'")
                print("Seleccione nuevo estado:\n 1. Pendiente\n 2. En ruta\n 3. Entregado\n 4. Cancelado")
                est_opc = input("Opción (1-4): ").strip()
                estados_map = {"1": "Pendiente", "2": "En ruta", "3": "Entregado", "4": "Cancelado"}
                
                if est_opc in estados_map:
                    p.estado = estados_map[est_opc]
                    print(f"Estado actualizado con éxito a: '{p.estado}'.")
                else:
                    print("Selección inválida.")
            else:
                print("Paquete no encontrado en el sistema.")
                
        elif op == "6":
            print("\nPlanificación De Ruta Inteligente (DFS)")
            cod = input("Código del paquete a despachar: ").strip()
            p = paquetes.get(cod)
            if p:
                nombre_rep = input("Nombre del repartidor asignado: ").strip()
                rep = repartidores.get(nombre_rep)
                if rep:
                    # Invocar algoritmo DFS recursivo pasándole origen y destino
                    resultado = ciudad.buscar_ruta_dfs(rep.zona_actual, p.destino)
                    if resultado:
                        ruta_exacta, km_totales = resultado
                        print(f"\n¡Ruta calculada para {rep.nombre}!")
                        print(f"Camino: {' -> '.join(ruta_exacta)}")
                        print(f"Distancia de trayecto: {km_totales} km")
                        
                        # Simular asignación logística automática
                        if p not in rep.paquetes_asignados:
                            rep.paquetes_asignados.append(p)
                            p.estado = "En ruta"
                            
                            rep.zona_actual = p.destino
                            
                            print(f"El paquete ha sido cargado al vehículo. Su estado cambió a 'En ruta' y '{rep.nombre}' se movió a {rep.zona_actual}.")

                    else:
                        print(f"Error en grafos: No existe conexión vial directa entre '{rep.zona_actual}' y '{p.destino}'.")
                else:
                    print("El repartidor especificado no existe.")
            else:
                print("Paquete no encontrado.")
                
        elif op == "7":
            print("\nReporte De Repartidor (Ordenado por peso)")
            nombre = input("Nombre del repartidor a consultar: ").strip()
            rep = repartidores.get(nombre)
            if rep:
                print(f"\nManifiesto de carga para: {rep.nombre} ({rep.vehiculo})")
                print(f"Ubicación actual: {rep.zona_actual}")
                print("-" * 50)
                
                paquetes_ordenados = ordenar_paquetes_por_peso(rep.paquetes_asignados)
                if not paquetes_ordenados:
                    print("No tiene paquetes asignados en este momento.")
                for p in paquetes_ordenados:
                    print(f" - [Paquete {p.codigo}] Peso: {p.peso} kg -> Destino: {p.destino} ({p.estado})")
            else:
                print("Repartidor no encontrado.")
                
        elif op == "8":
            # Persistencia de datos al cerrar el programa
            guardar_a_csv(clientes, paquetes, repartidores)
            print("\nCambios guardados correctamente en la carpeta /data/.")
            print("Saliendo del sistema logístico de entregas. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()

