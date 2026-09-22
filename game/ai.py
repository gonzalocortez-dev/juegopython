"""IA del equipo rojo: simple y facil de explicar.

Idea: para que la pelota salga hacia el arco rival hay que golpearla desde
el lado opuesto. Entonces la IA busca ese "punto de golpe" y lanza hacia ahi
al jugador que lo tenga mas cerca.
"""

import random

import pygame

import settings as s


def elegir_tiro(jugadores, pelota, cancha, equipo="rojo"):
    """Devuelve (jugador, direccion, fuerza) para el turno de la CPU."""
    arco_rival = cancha.centro_arco(equipo)

    # 1) Direccion en la que queremos que salga la pelota.
    hacia_el_arco = arco_rival - pelota.pos
    if hacia_el_arco.length() == 0:
        hacia_el_arco = pygame.Vector2(-1, 0)
    hacia_el_arco = hacia_el_arco.normalize()

    # 2) Punto justo detras de la pelota: desde ahi el golpe la manda al arco.
    punto_de_golpe = pelota.pos - hacia_el_arco * (pelota.radio + s.RADIO_JUGADOR)

    # 3) El jugador que mas cerca este de ese punto es el que patea.
    jugador = min(jugadores, key=lambda j: j.pos.distance_to(punto_de_golpe))

    direccion = punto_de_golpe - jugador.pos
    if direccion.length() == 0:
        direccion = hacia_el_arco
    direccion = direccion.normalize()

    # 4) Punteria imperfecta a proposito: hace que la CPU no sea invencible.
    direccion = direccion.rotate(random.uniform(-7, 7))

    # 5) Fuerza proporcional a la distancia, con un minimo para que siempre llegue.
    distancia = jugador.pos.distance_to(punto_de_golpe)
    fuerza = min(distancia + 160, s.DISTANCIA_MAXIMA_TIRO) * s.FUERZA_POR_PIXEL
    return jugador, direccion, fuerza
