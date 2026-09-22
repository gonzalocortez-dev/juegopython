"""La cancha: se dibuja con primitivas de pygame (sin imagenes externas)."""

import pygame

import settings as s


class Field:
    """Guarda las medidas de la cancha y sabe dibujarla y detectar goles."""

    def __init__(self):
        # Rectangulo de juego: todo lo que este adentro es cancha valida.
        self.rect = pygame.Rect(
            s.MARGEN_X,
            s.MARGEN_SUPERIOR,
            s.ANCHO - 2 * s.MARGEN_X,
            s.ALTO - s.MARGEN_SUPERIOR - s.MARGEN_INFERIOR,
        )

        # Boca de cada arco: un tramo vertical centrado en cada lateral.
        self.arco_arriba = self.rect.centery - s.ALTO_ARCO // 2
        self.arco_abajo = self.rect.centery + s.ALTO_ARCO // 2

        # Arco izquierdo = lo defiende el equipo azul, derecho = el rojo.
        self.arco_izquierdo = pygame.Rect(
            self.rect.left - s.PROFUNDIDAD_ARCO, self.arco_arriba,
            s.PROFUNDIDAD_ARCO, s.ALTO_ARCO,
        )
        self.arco_derecho = pygame.Rect(
            self.rect.right, self.arco_arriba,
            s.PROFUNDIDAD_ARCO, s.ALTO_ARCO,
        )

    # --- Consultas ---

    def esta_en_boca_de_arco(self, y):
        """True si esa altura esta a la altura de los arcos (la pelota puede salir)."""
        return self.arco_arriba < y < self.arco_abajo

    def revisar_gol(self, pelota):
        """Devuelve 'azul', 'rojo' o None segun quien convirtio."""
        if pelota.pos.x + pelota.radio < self.rect.left:
            return "rojo"   # la pelota entro en el arco que defiende el azul
        if pelota.pos.x - pelota.radio > self.rect.right:
            return "azul"
        return None

    def centro_arco(self, equipo):
        """Centro del arco que ataca ese equipo (adonde hay que mandar la pelota)."""
        x = self.rect.right if equipo == "azul" else self.rect.left
        return pygame.Vector2(x, self.rect.centery)

    # --- Dibujo ---

    def dibujar(self, pantalla):
        pantalla.fill(s.VERDE_OSCURO)
        self._dibujar_cesped(pantalla)

        pygame.draw.rect(pantalla, s.BLANCO, self.rect, 4)

        # Linea y circulo central.
        pygame.draw.line(
            pantalla, s.BLANCO,
            (self.rect.centerx, self.rect.top),
            (self.rect.centerx, self.rect.bottom), 4,
        )
        pygame.draw.circle(pantalla, s.BLANCO, self.rect.center, 90, 4)
        pygame.draw.circle(pantalla, s.BLANCO, self.rect.center, 8)

        self._dibujar_areas(pantalla)
        self._dibujar_arcos(pantalla)

    def _dibujar_cesped(self, pantalla):
        """Franjas de cesped: solo decoracion, ayuda a ver el movimiento."""
        franja = self.rect.width // 8
        for i in range(8):
            if i % 2 == 0:
                continue
            pygame.draw.rect(
                pantalla, s.VERDE_CANCHA,
                (self.rect.left + i * franja, self.rect.top, franja, self.rect.height),
            )

    def _dibujar_areas(self, pantalla):
        ancho_area = 130
        alto_area = s.ALTO_ARCO + 120
        y = self.rect.centery - alto_area // 2
        pygame.draw.rect(
            pantalla, s.BLANCO, (self.rect.left, y, ancho_area, alto_area), 3)
        pygame.draw.rect(
            pantalla, s.BLANCO,
            (self.rect.right - ancho_area, y, ancho_area, alto_area), 3)

    def _dibujar_arcos(self, pantalla):
        for arco, color in ((self.arco_izquierdo, s.AZUL), (self.arco_derecho, s.ROJO)):
            pygame.draw.rect(pantalla, s.NEGRO, arco)
            pygame.draw.rect(pantalla, color, arco, 5)
