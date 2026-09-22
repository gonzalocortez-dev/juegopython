"""Los jugadores: fichas circulares que se lanzan para golpear la pelota."""

import pygame

import settings as s


class Player:
    def __init__(self, x, y, equipo):
        self.pos = pygame.Vector2(x, y)
        self.inicio = pygame.Vector2(x, y)  # posicion de saque, para reiniciar
        self.vel = pygame.Vector2(0, 0)
        self.equipo = equipo                # "azul" o "rojo"
        self.radio = s.RADIO_JUGADOR
        self.masa = 3.0                     # mas pesado que la pelota
        self.color = s.AZUL if equipo == "azul" else s.ROJO
        self.seleccionado = False

    @property
    def detenido(self):
        return self.vel.length() < s.VELOCIDAD_MINIMA

    def contiene(self, punto):
        """True si el punto (por ejemplo el mouse) cae dentro de la ficha."""
        return self.pos.distance_to(punto) <= self.radio

    def lanzar(self, direccion, fuerza):
        self.vel = direccion * fuerza
        if self.vel.length() > s.VELOCIDAD_MAXIMA:
            self.vel.scale_to_length(s.VELOCIDAD_MAXIMA)

    def volver_al_inicio(self):
        self.pos.update(self.inicio)
        self.vel.update(0, 0)
        self.seleccionado = False

    def actualizar(self, dt, cancha):
        self.pos += self.vel * dt
        self.vel *= s.FRICCION ** (dt * s.FPS)
        if self.detenido:
            self.vel.update(0, 0)

        # Los jugadores nunca salen de la cancha: siempre rebotan.
        if self.pos.x - self.radio < cancha.rect.left:
            self.pos.x = cancha.rect.left + self.radio
            self.vel.x = -self.vel.x * s.REBOTE_PARED
        elif self.pos.x + self.radio > cancha.rect.right:
            self.pos.x = cancha.rect.right - self.radio
            self.vel.x = -self.vel.x * s.REBOTE_PARED

        if self.pos.y - self.radio < cancha.rect.top:
            self.pos.y = cancha.rect.top + self.radio
            self.vel.y = -self.vel.y * s.REBOTE_PARED
        elif self.pos.y + self.radio > cancha.rect.bottom:
            self.pos.y = cancha.rect.bottom - self.radio
            self.vel.y = -self.vel.y * s.REBOTE_PARED

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, self.pos, self.radio)
        pygame.draw.circle(pantalla, s.BLANCO, self.pos, self.radio, 3)
        if self.seleccionado:
            pygame.draw.circle(pantalla, s.AMARILLO, self.pos, self.radio + 7, 3)


def formacion(equipo, cancha):
    """Posiciones iniciales de un equipo (5 fichas, espejadas segun el lado)."""
    # Porcentajes del ancho/alto de la cancha: asi funciona con cualquier tamano.
    puntos = [
        (0.08, 0.50),  # arquero
        (0.25, 0.25),
        (0.25, 0.75),
        (0.40, 0.40),
        (0.40, 0.60),
    ]
    jugadores = []
    for px, py in puntos:
        if equipo == "rojo":
            px = 1 - px  # el rojo juega del lado derecho
        x = cancha.rect.left + px * cancha.rect.width
        y = cancha.rect.top + py * cancha.rect.height
        jugadores.append(Player(x, y, equipo))
    return jugadores
