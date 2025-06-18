import pygame
from pygame.locals import *


class EventHandler:
    @staticmethod
    def procesar_eventos(particula_manager):
        eventos = {
            "salir": False,
            "reiniciar": False,
            "particula_seleccionada": None,
            "mostrar_distancias": True,
        }

        for evento in pygame.event.get():
            if evento.type == QUIT:
                eventos["salir"] = True
            elif evento.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i in range(particula_manager.num_particulas):
                    dx = x - particula_manager.posiciones[i, 0]
                    dy = y - particula_manager.posiciones[i, 1]
                    if dx**2 + dy**2 <= particula_manager.radios[i] ** 2:
                        eventos["particula_seleccionada"] = i
                        break
                else:
                    eventos["particula_seleccionada"] = None
            elif evento.type == KEYDOWN:
                if evento.key == K_SPACE:
                    eventos["mostrar_distancias"] = not eventos["mostrar_distancias"]
                elif evento.key == K_r:
                    eventos["reiniciar"] = True
                elif evento.key == K_ESCAPE:
                    eventos["particula_seleccionada"] = None
        return eventos
