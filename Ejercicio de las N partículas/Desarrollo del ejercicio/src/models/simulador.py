import pygame
import sys
from pygame.locals import *
from particula_manager import ParticulaManager
from renderer import Renderer
from event_handler import EventHandler
from constants import ANCHO, ALTO, FPS


# Clase principal que coordina toda la simulación
class Simulador:
    # Constructor: inicializa pygame y los componentes principales
    def __init__(self, num_particulas=15):
        pygame.init()
        # Configura la ventana de visualización
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Distancias Mínimas entre Partículas")
        self.fuente = pygame.font.SysFont("Arial", 12)
        # Inicializa los gestores de partículas y renderizado
        self.particula_manager = ParticulaManager(num_particulas)
        self.renderer = Renderer(self.pantalla, self.fuente)
        self.reloj = pygame.time.Clock()

    # Bucle principal de la simulación
    def ejecutar(self):
        while True:
            # Procesa los eventos de usuario (teclado, ratón, etc.)
            eventos = EventHandler.procesar_eventos(self.particula_manager)
            if eventos["salir"]:
                pygame.quit()
                sys.exit()
            if eventos["reiniciar"]:
                self.particula_manager.inicializar_particulas()

            # Actualiza la física de las partículas
            self.particula_manager.actualizar_fisica()
            # Limpia la pantalla para el nuevo frame
            self.renderer.limpiar_pantalla()

            # Renderiza las partículas
            self.renderer.dibujar_particulas(
                self.particula_manager.posiciones, self.particula_manager.radios
            )

            # Renderiza la línea de distancia mínima si existe
            if self.particula_manager.par_mas_cercano[0] is not None:
                self.renderer.dibujar_linea_minima(
                    self.particula_manager.posiciones,
                    self.particula_manager.par_mas_cercano,
                    self.particula_manager.min_distancia,
                )
                self.renderer.dibujar_distancia_minima_arriba(
                    self.particula_manager.min_distancia
                )

            # Actualiza la pantalla y mantiene el framerate constante
            pygame.display.flip()
            self.reloj.tick(FPS)


# Punto de entrada del programa
if __name__ == "__main__":
    while True:
        try:
            num_particulas = int(input("Por favor, ingrese el número de partículas: "))
            if num_particulas > 0:
                break
            else:
                print("El número debe ser positivo.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

    sim = Simulador(num_particulas)
    sim.ejecutar()
