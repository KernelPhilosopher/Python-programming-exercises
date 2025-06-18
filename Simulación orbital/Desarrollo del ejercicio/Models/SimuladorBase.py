import math


class SimuladorBase:
    G = 6.6748e-11  # Constante gravitacional
    M_SOL = 1.989e30  # Masa del Sol (kg)
    UA = 1.496e11  # 1 UA en metros

    def __init__(self, dt=86400, velocidad_inicial=29783):
        self.dt = dt  # Paso de tiempo (1 día)
        self.x = self.UA  # Posición inicial en X
        self.y = 0.0  # Posición inicial en Y
        self.vx = 0.0  # Velocidad inicial en X
        self.vy = velocidad_inicial  # Velocidad inicial en Y
        self.t_total = dt * 365  # 1 año en segundos
        self.x_vals = []
        self.y_vals = []

    def calcular_aceleracion(self, x, y):
        r = math.sqrt(x**2 + y**2)
        a_mag = -self.G * self.M_SOL / r**3
        ax = a_mag * x
        ay = a_mag * y
        return ax, ay

    def simular(self):
        raise NotImplementedError("Método simular debe ser implementado en subclases")
