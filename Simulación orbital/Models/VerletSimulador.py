from .SimuladorBase import SimuladorBase


class VerletSimulador(SimuladorBase):
    def simular(self):
        t = 0
        while t < self.t_total:
            ax, ay = self.calcular_aceleracion(self.x, self.y)

            # Actualizar posiciones
            x_nuevo = self.x + self.vx * self.dt + 0.5 * ax * self.dt**2
            y_nuevo = self.y + self.vy * self.dt + 0.5 * ay * self.dt**2

            # Calcular nueva aceleración
            ax_nuevo, ay_nuevo = self.calcular_aceleracion(x_nuevo, y_nuevo)

            # Actualizar velocidades
            self.vx += 0.5 * (ax + ax_nuevo) * self.dt
            self.vy += 0.5 * (ay + ay_nuevo) * self.dt

            self.x = x_nuevo
            self.y = y_nuevo
            self.x_vals.append(self.x)
            self.y_vals.append(self.y)
            t += self.dt
