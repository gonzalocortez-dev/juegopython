"""Menu principal y pantalla de instrucciones.

Devuelven una accion ("jugar", "instrucciones", "menu", "salir" o None) para
que main.py decida que pantalla mostrar. Toda la interfaz se dibuja con
pygame.draw y pygame.font: no hay imagenes que descargar.
"""

import math

import pygame

import settings as s
from game import ui
from game.ui import Boton


class Menu:
    def __init__(self):
        self.botones = [
            (Boton("JUGAR", (s.ANCHO // 2, 400)), "jugar"),
            (Boton("INSTRUCCIONES", (s.ANCHO // 2, 480)), "instrucciones"),
            (Boton("SALIR", (s.ANCHO // 2, 560)), "salir"),
        ]
        self.tiempo = 0.0

    def procesar_evento(self, evento):
        for boton, accion in self.botones:
            if boton.procesar_evento(evento):
                return accion
        return None

    def actualizar(self, dt):
        self.tiempo += dt

    def dibujar(self, pantalla):
        _fondo(pantalla, self.tiempo)

        centro_x = s.ANCHO // 2
        # La pelota del titulo se dibuja con circulos (la fuente del sistema
        # no tiene emojis en el navegador).
        pygame.draw.circle(pantalla, s.BLANCO, (centro_x - 330, 200), 26)
        pygame.draw.circle(pantalla, s.NEGRO, (centro_x - 330, 200), 26, 3)
        pygame.draw.circle(pantalla, s.NEGRO, (centro_x - 330, 200), 9)
        ui.texto_centrado(pantalla, "FÚTBOL DE MESA", 96, s.TEXTO, (centro_x, 200))
        ui.texto_centrado(pantalla, "Azul (vos) contra Rojo (CPU) — 3 goles ganan",
                          32, s.TEXTO_SUAVE, (centro_x, 275))

        for boton, _ in self.botones:
            boton.dibujar(pantalla)

        ui.texto_centrado(pantalla, "Hecho con Python + pygame-ce, en el navegador con pygbag",
                          26, s.TEXTO_SUAVE, (centro_x, s.ALTO - 40))


class Instrucciones:
    LINEAS = [
        "1. Hace click en una de tus fichas azules para elegirla.",
        "2. Movés el mouse: la flecha muestra la dirección y la barra la potencia.",
        "3. Segundo click: la ficha sale disparada y empuja la pelota.",
        "4. Cuando todo se detiene, juega la CPU (equipo rojo).",
        "5. Si la pelota entra en el arco rival, es gol.",
        "6. Gana el primero que llega a 3 goles. Con R volvés a empezar.",
    ]

    def __init__(self):
        self.volver = Boton("VOLVER", (s.ANCHO // 2, 620), ancho=240, alto=56)
        self.tiempo = 0.0

    def procesar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"
        if self.volver.procesar_evento(evento):
            return "menu"
        return None

    def actualizar(self, dt):
        self.tiempo += dt

    def dibujar(self, pantalla):
        _fondo(pantalla, self.tiempo)

        centro_x = s.ANCHO // 2
        ui.texto_centrado(pantalla, "CÓMO SE JUEGA", 72, s.TEXTO, (centro_x, 130))

        panel = pygame.Rect(0, 0, 940, 330)
        panel.center = (centro_x, 380)
        pygame.draw.rect(pantalla, s.PANEL, panel, border_radius=18)
        pygame.draw.rect(pantalla, s.BOTON_BORDE, panel, 2, border_radius=18)

        y = panel.top + 45
        for linea in self.LINEAS:
            texto = ui.fuente(32).render(linea, True, s.TEXTO)
            pantalla.blit(texto, (panel.left + 45, y))
            y += 48

        self.volver.dibujar(pantalla)


def _fondo(pantalla, tiempo):
    """Fondo oscuro con una cancha insinuada: barato de dibujar y con identidad."""
    pantalla.fill(s.FONDO)

    borde = pygame.Rect(60, 60, s.ANCHO - 120, s.ALTO - 120)
    pygame.draw.rect(pantalla, s.LINEA_TENUE, borde, 2, border_radius=8)
    pygame.draw.line(pantalla, s.LINEA_TENUE,
                     (borde.centerx, borde.top), (borde.centerx, borde.bottom), 2)
    radio = 120 + int(6 * math.sin(tiempo * 2))
    pygame.draw.circle(pantalla, s.LINEA_TENUE, borde.center, radio, 2)
