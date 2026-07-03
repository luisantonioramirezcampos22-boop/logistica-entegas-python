class CiudadGrafo:
    def __init__(self, estructura_grafo):
        # Aqui recibe el diccionario cargado desde el JSON
        self.grafo = estructura_grafo

    def buscar_ruta_dfs(self, actual, destino, visitados=None, ruta=None, distancia_total=0):
        if visitados is None:
            visitados = set()
        if ruta is None:
            ruta = []

        visitados.add(actual)
        ruta.append(actual)

        if actual == destino:
            return ruta, distancia_total

        for vecino, distancia_calle in self.grafo.get(actual, {}).items():
            if vecino not in visitados:
                resultado = self.buscar_ruta_dfs(
                    vecino, 
                    destino, 
                    visitados.copy(), 
                    ruta.copy(), 
                    distancia_total + distancia_calle
                )
                if resultado:
                    return resultado
        return None

