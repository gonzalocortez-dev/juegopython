"""Piezas visuales compartidas: fuentes y botones.

Las fuentes se crean una sola vez y se guardan en un diccionario (cache):
crear una fuente es la operacion mas cara del arranque en el navegador.
"""

import pygame

import settings as s

_fuentes = {}


def fuente(tamano):
    """Devuelve una fuente del tamano pedido, reutilizandola si ya existe."""
    if tamano not in _fuentes:
        _fuentes[tamano] = pygame.font.Font(None, tamano)
    return _fuentes[tamano]


def texto_centrado(pantalla, texto, tamano, color, centro):
    superficie = fuente(tamano).render(texto, True, color)
    pantalla.blit(superficie, superficie.get_rect(center=centro))
    return superficie


class Boton:
    """Boton rectangular que reacciona al mouse (hover y click)."""

    def __init__(self, texto, centro, ancho=320, alto=62):
        self.texto = texto
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = centro
        self.encima = False    # el mouse esta arriba
        self.apretado = False  # el boton del mouse esta hundido

    def procesar_evento(self, evento):
        """Devuelve True cuando el click se completa sobre el boton."""
        if evento.type == pygame.MOUSEMOTION:
            self.encima = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            self.encima = self.rect.collidepoint(evento.pos)
            self.apretado = self.encima
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            activado = self.apretado and self.rect.collidepoint(evento.pos)
            self.apretado = False
            return activado
        return False

    def dibujar(self, pantalla):
        # El feedback visual es solo un cambio de color y un pequeno
        # desplazamiento: se entiende de un vistazo y no cuesta nada dibujarlo.
        rect = self.rect.move(0, 2) if self.apretado else self.rect
        if self.apretado:
            color = s.BOTON_APRETADO
        elif self.encima:
            color = s.BOTON_ENCIMA
        else:
            color = s.BOTON

        pygame.draw.rect(pantalla, color, rect, border_radius=14)
        pygame.draw.rect(pantalla, s.BOTON_BORDE, rect, 2, border_radius=14)
        texto_centrado(pantalla, self.texto, 40, s.TEXTO, rect.center)
