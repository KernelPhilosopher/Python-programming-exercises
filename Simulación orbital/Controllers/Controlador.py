class Controlador:
    def __init__(self, simulador, vista):
        self.simulador = simulador
        self.vista = vista

    def ejecutar_simulacion(self):
        self.simulador.simular()
        self.vista.configurar_grafico()
        self.vista.animar()
