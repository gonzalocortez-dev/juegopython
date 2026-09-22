"""La pelota: posicion, velocidad, friccion y rebote contra los bordes."""

import pygame

import settings as s


class Ball:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.radio = s.RADIO_PELOTA
        self.masa = 1.0  # liviana: los jugadores la empujan facil

    @property
    def detenida(self):
        return self.vel.length() < s.VELOCIDAD_MINIMA

    def patear(self, direccion, fuerza):
        """Suma velocidad en una direccion (se espera un vector normalizado)."""
        self.vel += direccion * fuerza
        if self.vel.length() > s.VELOCIDAD_MAXIMA:
            self.vel.scale_to_length(s.VELOCIDAD_MAXIMA)

    def actualizar(self, dt, cancha):
        # 1) Se mueve segun su velocidad.
        self.pos += self.vel * dt

        # 2) La friccion la va frenando de a poco hasta detenerla.
        self.vel *= s.FRICCION ** (dt * s.FPS)
        if self.detenida:
            self.vel.update(0, 0)

        self._rebotar_en_bordes(cancha)

    def _rebotar_en_bordes(self, cancha):
        """Rebota contra las lineas, salvo cuando pasa por la boca del arco."""
        pasando_por_arco = cancha.esta_en_boca_de_arco(self.pos.y)

        if not pasando_por_arco:
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
        pygame.draw.circle(pantalla, s.BLANCO, self.pos, self.radio)
        pygame.draw.circle(pantalla, s.NEGRO, self.pos, self.radio, 2)
