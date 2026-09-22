"""Pantalla de carga del juego (la que se ve dentro del canvas de pygame).

Progreso REAL: cada etapa es una funcion que hace trabajo de verdad
(crear la cancha, las fichas, los sonidos...). El porcentaje es
etapas_terminadas / etapas_totales, no un reloj decorativo.

Ejecutamos una sola etapa por frame y despues dibujamos: asi el navegador
nunca se congela y la barra avanza a medida que el juego se arma.
"""

import math

import pygame

import settings as s
from game import ui


class PantallaCarga:
    def __init__(self, etapas):
        # etapas = lista de (mensaje, funcion)
        self.etapas = etapas
        self.hechas = 0
        self.mensaje = "Iniciando..."
        self.progreso_dibujado = 0.0  # la barra persigue al progreso real
        self.tiempo = 0.0
        self.espera_final = 0.0

    @property
    def progreso(self):
        """Valor real entre 0 y 1."""
        return self.hechas / len(self.etapas)

    @property
    def listo(self):
        """True cuando termino todo y ya se mostro el cartel final."""
        return self.hechas == len(self.etapas) and self.espera_final <= 0

    def actualizar(self, dt):
        self.tiempo += dt

        # 1) Una etapa por frame: el trabajo real que mueve la barra.
        if self.hechas < len(self.etapas):
            mensaje, tarea = self.etapas[self.hechas]
            if self.mensaje != mensaje:
                # Primero mostramos el mensaje y recien al frame siguiente
                # hacemos el trabajo: asi cada etapa se llega a leer.
                self.mensaje = mensaje
            else:
                tarea()
                self.hechas += 1
                if self.hechas == len(self.etapas):
                    self.mensaje = "¡Todo listo!"
                    self.espera_final = s.ESPERA_TODO_LISTO
        else:
            # 2) Cartel "¡Todo listo!" un instante, sin time.sleep().
            self.espera_final -= dt

        # La barra se acerca suavemente al valor real (queda mas prolijo).
        self.progreso_dibujado += (self.progreso - self.progreso_dibujado) * min(1, dt * 8)

    def dibujar(self, pantalla):
        pantalla.fill(s.FONDO)

        centro_x = s.ANCHO // 2

        # Pelota dibujada con circulos (sin imagenes externas) que "late".
        latido = 1 + 0.06 * math.sin(self.tiempo * 4)
        radio = int(34 * latido)
        pygame.draw.circle(pantalla, s.BLANCO, (centro_x, 210), radio)
        pygame.draw.circle(pantalla, s.NEGRO, (centro_x, 210), radio, 3)
        pygame.draw.circle(pantalla, s.NEGRO, (centro_x, 210), max(4, radio // 3))

        ui.texto_centrado(pantalla, "FÚTBOL DE MESA", 78, s.TEXTO, (centro_x, 310))
        ui.texto_centrado(pantalla, "Preparando el partido...", 34, s.TEXTO_SUAVE,
                          (centro_x, 365))

        self._dibujar_barra(pantalla, centro_x, 430)

        ui.texto_centrado(pantalla, self.mensaje, 32, s.TEXTO, (centro_x, 490))
        ui.texto_centrado(pantalla, "Python + pygame-ce + pygbag", 26, s.TEXTO_SUAVE,
                          (centro_x, s.ALTO - 40))

    def _dibujar_barra(self, pantalla, centro_x, y):
        ancho, alto = 560, 26
        fondo = pygame.Rect(centro_x - ancho // 2, y, ancho, alto)
        pygame.draw.rect(pantalla, s.BARRA_FONDO, fondo, border_radius=13)

        relleno = fondo.copy()
        relleno.width = int(ancho * self.progreso_dibujado)
        if relleno.width > 6:
            pygame.draw.rect(pantalla, s.BARRA, relleno, border_radius=13)
        pygame.draw.rect(pantalla, s.BARRA_BORDE, fondo, 2, border_radius=13)

        porcentaje = f"{int(self.progreso * 100)}%"
        ui.texto_centrado(pantalla, porcentaje, 28, s.TEXTO,
                          (fondo.right + 42, fondo.centery))
