import numpy as np
from quadtree_node import QuadtreeNode
from constants import G, MAX_PARTICULAS_NODO, ANCHO, ALTO


# Clase que gestiona la física y el comportamiento de las partículas en la simulación
class ParticulaManager:
    # Constructor: inicializa el sistema con un número específico de partículas
    def __init__(self, num_particulas):
        self.num_particulas = num_particulas
        self.min_distancia = float("inf")
        self.par_mas_cercano = (
            None,
            None,
        )  # Almacena los índices de las partículas más cercanas
        self.inicializar_particulas()

    # Método para crear y configurar las partículas iniciales
    def inicializar_particulas(self):
        # Genera posiciones aleatorias dentro de los límites de la pantalla
        self.posiciones = np.random.rand(self.num_particulas, 2)
        self.posiciones[:, 0] *= ANCHO
        self.posiciones[:, 1] *= ALTO
        # Genera velocidades aleatorias con componentes entre -2 y 2
        self.velocidades = (np.random.rand(self.num_particulas, 2) - 0.5) * 4
        # Genera masas aleatorias entre 5 y 15
        self.masas = np.random.rand(self.num_particulas) * 10 + 5
        # El radio de cada partícula es proporcional a su masa
        self.radios = self.masas / 2

    # Método para construir el árbol cuaternario (quadtree) para optimización espacial
    def construir_quadtree(self):
        root = QuadtreeNode(0, 0, ANCHO, ALTO, max_particulas=MAX_PARTICULAS_NODO)
        for i in range(self.num_particulas):
            part = {"id": i, "pos": tuple(self.posiciones[i])}
            root.insertar(part)
        return root

    # Método principal que actualiza la física del sistema
    def actualizar_fisica(self):
        n = self.num_particulas
        # Array para almacenar las aceleraciones de cada partícula
        aceleraciones = np.zeros((n, 2))
        self.min_distancia = float("inf")
        self.par_mas_cercano = (None, None)

        # Cálculo de fuerzas gravitacionales entre todas las partículas
        for i in range(n):
            for j in range(i + 1, n):
                # Calcula la distancia entre partículas
                dx = self.posiciones[j, 0] - self.posiciones[i, 0]
                dy = self.posiciones[j, 1] - self.posiciones[i, 1]
                dist = np.sqrt(dx**2 + dy**2)

                # Actualiza el par más cercano si corresponde
                if dist < self.min_distancia:
                    self.min_distancia = dist
                    self.par_mas_cercano = (i, j)

                # Previene superposición excesiva estableciendo una distancia mínima
                dist = max(dist, 2 * max(self.radios[i], self.radios[j]))
                # Calcula la fuerza gravitacional
                fuerza = G * self.masas[i] * self.masas[j] / (dist**2)
                # Actualiza las aceleraciones según la ley de Newton
                aceleraciones[i] += fuerza * np.array([dx, dy]) / (dist * self.masas[i])
                aceleraciones[j] -= fuerza * np.array([dx, dy]) / (dist * self.masas[j])

        # Actualiza velocidades y posiciones usando las aceleraciones calculadas
        self.velocidades += aceleraciones
        self.posiciones += self.velocidades

        # Manejo de colisiones con los bordes de la pantalla
        for i in range(n):
            for dim in range(2):
                limite = ANCHO if dim == 0 else ALTO
                # Rebote en los bordes con pérdida de energía (factor 0.9)
                if (
                    self.posiciones[i, dim] < self.radios[i]
                    or self.posiciones[i, dim] > limite - self.radios[i]
                ):
                    self.velocidades[i, dim] *= -0.9
            # Asegura que las partículas permanezcan dentro de los límites
            self.posiciones[i] = np.clip(
                self.posiciones[i],
                self.radios[i],
                [ANCHO - self.radios[i], ALTO - self.radios[i]],
            )
