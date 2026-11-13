import numpy as np

class ColoniaHormigas:
    def __init__(self, distancias, n_hormigas, n_iteraciones, evaporacion, alfa=1.0, beta=2.0):
        self.distancias = distancias
        self.n_hormigas = n_hormigas
        self.n_iteraciones = n_iteraciones
        self.evaporacion = evaporacion
        self.alfa = alfa
        self.beta = beta
        self.n_nodos = len(distancias)
        self.feromonas = np.ones((self.n_nodos, self.n_nodos))

    def ejecutar(self):
        mejor_camino = None
        mejor_distancia = float('inf')

        for _ in range(self.n_iteraciones):
            caminos = self._generar_caminos()
            self._actualizar_feromonas(caminos)

            for camino, distancia in caminos:
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_camino = camino

        return mejor_camino, mejor_distancia

    def _generar_caminos(self):
        caminos = []
        for _ in range(self.n_hormigas):
            camino = self._construir_camino_hormiga()
            distancia = self._calcular_distancia(camino)
            caminos.append((camino, distancia))
        return caminos

    def _construir_camino_hormiga(self):
        nodo_actual = np.random.randint(self.n_nodos) 
        camino = [nodo_actual]
        visitados = set(camino)

        while len(visitados) < self.n_nodos:
            probabilidades = self._calcular_probabilidades(nodo_actual, visitados)
            siguiente_nodo = np.random.choice(range(self.n_nodos), p=probabilidades)
            camino.append(siguiente_nodo)
            visitados.add(siguiente_nodo)
            nodo_actual = siguiente_nodo

        camino.append(camino[0])
        return camino

    def _calcular_probabilidades(self, nodo_actual, visitados):
        probabilidades = np.zeros(self.n_nodos)
        for i in range(self.n_nodos):
            if i not in visitados:
                feromona = self.feromonas[nodo_actual][i] ** self.alfa
                visibilidad = (1.0 / self.distancias[nodo_actual][i]) ** self.beta
                probabilidades[i] = feromona * visibilidad

        return probabilidades / probabilidades.sum()

    def _calcular_distancia(self, camino):
        distancia = 0
        for i in range(len(camino) - 1):
            distancia += self.distancias[camino[i]][camino[i+1]]
        return distancia

    def _actualizar_feromonas(self, caminos):
        self.feromonas *= (1 - self.evaporacion)

        for camino, distancia in caminos:
            aporte_feromona = 1.0 / distancia
            for i in range(len(camino) - 1):
                nodo_a, nodo_b = camino[i], camino[i+1]
                self.feromonas[nodo_a][nodo_b] += aporte_feromona
                self.feromonas[nodo_b][nodo_a] += aporte_feromona

if __name__ == '__main__':
    distancias_ciudades = np.array([
        [np.inf, 2, 2, 5, 7],
        [2, np.inf, 4, 8, 2],
        [2, 4, np.inf, 1, 3],
        [5, 8, 1, np.inf, 2],
        [7, 2, 3, 2, np.inf]
    ])

    aco = ColoniaHormigas(
        distancias=distancias_ciudades, 
        n_hormigas=10, 
        n_iteraciones=50, 
        evaporacion=0.1, 
        alfa=1.0, 
        beta=2.0
    )
    
    mejor_ruta, menor_distancia = aco.ejecutar()
    print(f"La mejor ruta encontrada es: {mejor_ruta}")
    print(f"Distancia total de la ruta: {menor_distancia}")
