import matplotlib.pyplot as plt
import matplotlib.animation as animation


class VistaOrbital:
    def __init__(self, simulador):
        self.simulador = simulador
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

    def configurar_grafico(self):
        self.ax.set_xlim(-1.6 * self.simulador.UA, 1.6 * self.simulador.UA)
        self.ax.set_ylim(-1.6 * self.simulador.UA, 1.6 * self.simulador.UA)
        self.ax.scatter(0, 0, color="yellow", s=100, label="Sol")
        self.ax.set_title("Simulación Orbital")
        self.ax.legend()

    def animar(self):
        def update(frame):
            self.ax.clear()
            self.configurar_grafico()
            self.ax.plot(
                self.simulador.x_vals[:frame],
                self.simulador.y_vals[:frame],
                color="blue",
                label="Órbita",
            )

        ani = animation.FuncAnimation(
            self.fig, update, frames=len(self.simulador.x_vals), interval=20
        )
        plt.show()
