import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

def cargar_grafo_json():
    path_j = os.path.join(DATA_DIR, 'rutas.json')
    if os.path.exists(path_j):
        with open(path_j, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {} # Retorna vacío si el archivo no existe

