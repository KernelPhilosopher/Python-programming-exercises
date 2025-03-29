from .SimuladorBase import SimuladorBase


class EulerSimulador(SimuladorBase):
    def simular(self):
        t = 0
        while t < self.t_total:
            ax, ay = self.calcular_aceleracion(self.x, self.y)
            self.vx += ax * self.dt
            self.vy += ay * self.dt
            self.x += self.vx * self.dt
            self.y += self.vy * self.dt
            self.x_vals.append(self.x)
            self.y_vals.append(self.y)
            t += self.dt
