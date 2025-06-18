import numpy as np


class QuadtreeNode:
    def __init__(self, x_min, y_min, x_max, y_max, profundidad=0, max_particulas=4):
        self.limite = (x_min, y_min, x_max, y_max)
        self.profundidad = profundidad
        self.max_particulas = max_particulas
        self.particulas = []
        self.hijos = []

    def insertar(self, particula):
        if self.hijos:
            for hijo in self.hijos:
                if hijo.contiene(particula):
                    hijo.insertar(particula)
                    return
        else:
            self.particulas.append(particula)
            if len(self.particulas) > self.max_particulas:
                self.subdividir()
                for p in self.particulas:
                    for hijo in self.hijos:
                        if hijo.contiene(p):
                            hijo.insertar(p)
                            break
                self.particulas = []

    def contiene(self, particula):
        x, y = particula["pos"]
        x_min, y_min, x_max, y_max = self.limite
        return x_min <= x < x_max and y_min <= y < y_max

    def subdividir(self):
        x_min, y_min, x_max, y_max = self.limite
        mx = (x_min + x_max) / 2
        my = (y_min + y_max) / 2
        self.hijos = [
            QuadtreeNode(
                x_min, y_min, mx, my, self.profundidad + 1, self.max_particulas
            ),
            QuadtreeNode(
                mx, y_min, x_max, my, self.profundidad + 1, self.max_particulas
            ),
            QuadtreeNode(
                x_min, my, mx, y_max, self.profundidad + 1, self.max_particulas
            ),
            QuadtreeNode(
                mx, my, x_max, y_max, self.profundidad + 1, self.max_particulas
            ),
        ]

    def buscar_vecinos(self, particula, distancia_minima=float("inf")):
        x, y = particula["pos"]
        vecino = None
        if self.hijos:
            for hijo in self.hijos:
                if hijo.contiene(particula):
                    vecino, distancia_minima = hijo.buscar_vecinos(
                        particula, distancia_minima
                    )
                else:
                    distancia_al_cuadrante = hijo.distancia_a_cuadrante(x, y)
                    if distancia_al_cuadrante < distancia_minima:
                        v, d = hijo.buscar_vecinos(particula, distancia_minima)
                        if d < distancia_minima:
                            vecino, distancia_minima = v, d
        else:
            for p in self.particulas:
                if p["id"] != particula["id"]:
                    dx = p["pos"][0] - x
                    dy = p["pos"][1] - y
                    dist = (dx**2 + dy**2) ** 0.5
                    if dist < distancia_minima:
                        vecino, distancia_minima = p, dist
        return vecino, distancia_minima

    def distancia_a_cuadrante(self, x, y):
        x_min, y_min, x_max, y_max = self.limite
        dx = max(x_min - x, 0, x - x_max)
        dy = max(y_min - y, 0, y - y_max)
        return (dx**2 + dy**2) ** 0.5
