import pygame
from constants import COLORES, COLOR_FONDO


# Clase encargada de toda la renderización gráfica de la simulación
class Renderer:
    # Constructor: recibe la superficie de pygame y la fuente para el texto
    def __init__(self, pantalla, fuente):
        self.pantalla = pantalla
        self.fuente = fuente

    # Limpia la pantalla con el color de fondo
    def limpiar_pantalla(self):
        self.pantalla.fill(COLOR_FONDO)

    # Dibuja todas las partículas con sus números identificadores
    def dibujar_particulas(self, posiciones, radios):
        for i in range(len(posiciones)):
            # Asigna colores cíclicamente desde la lista de colores disponibles
            color = COLORES[i % len(COLORES)]
            # Dibuja el círculo que representa la partícula
            pygame.draw.circle(
                self.pantalla,
                color,
                (int(posiciones[i, 0]), int(posiciones[i, 1])),
                int(radios[i]),
            )
            # Renderiza y coloca el número identificador en el centro de la partícula
            texto = self.fuente.render(str(i), True, (255, 255, 255))
            self.pantalla.blit(
                texto,
                (
                    int(posiciones[i, 0] - texto.get_width() / 2),
                    int(posiciones[i, 1] - texto.get_height() / 2),
                ),
            )

    # Dibuja la línea entre el par de partículas más cercanas
    def dibujar_linea_minima(self, posiciones, par, distancia):
        if par[0] is None or par[1] is None:
            return

        i, j = par
        color_linea = (0, 255, 0)  # Color verde para la línea
        grosor = 3

        # Dibuja una línea entre las partículas más cercanas
        pygame.draw.line(
            self.pantalla,
            color_linea,
            (int(posiciones[i, 0]), int(posiciones[i, 1])),
            (int(posiciones[j, 0]), int(posiciones[j, 1])),
            grosor,
        )

        # Muestra la distancia en el punto medio de la línea
        medio_x = (posiciones[i, 0] + posiciones[j, 0]) / 2
        medio_y = (posiciones[i, 1] + posiciones[j, 1]) / 2
        texto = self.fuente.render(f"{distancia:.2f}px", True, color_linea)
        self.pantalla.blit(
            texto, (medio_x - texto.get_width() / 2, medio_y - texto.get_height() / 2)
        )

    # Muestra la distancia mínima en la parte superior de la pantalla
    def dibujar_distancia_minima_arriba(self, distancia):
        if distancia == float("inf"):
            return
        color_texto = (0, 200, 0)  # Verde más oscuro para mejor visibilidad
        texto = self.fuente.render(
            f"Distancia mínima: {distancia:.2f}px", True, color_texto
        )
        self.pantalla.blit(texto, (10, 10))
