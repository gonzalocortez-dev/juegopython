"""Punto de entrada del juego.

El bucle es asincrono (async/await) porque pygbag necesita devolverle el
control al navegador en cada frame. En la computadora funciona igual.

Pantallas: CARGA -> MENU (o INSTRUCCIONES) -> JUEGO.
"""

import asyncio

import pygame

import settings as s
from game import sonidos
from game.ball import Ball
from game.carga import PantallaCarga
from game.field import Field
from game.game import Game
from game.menu import Instrucciones, Menu
from game.player import formacion
from game.ui import fuente

CARGA, MENU, INSTRUCCIONES, JUEGO = "carga", "menu", "instrucciones", "juego"


class Recursos:
    """Caja donde la pantalla de carga va dejando lo que arma cada etapa."""

    cancha = None
    jugadores = None
    pelota = None
    partido = None


def etapas_de_carga(pantalla, recursos):
    """Las etapas reales de inicializacion, en orden.

    Cada una es (mensaje, funcion): la pantalla de carga ejecuta una por
    frame y calcula el porcentaje como etapas_hechas / etapas_totales.
    """

    def preparar_fuentes():
        for tamano in (26, 32, 34, 40, 64, 72, 78, 96):
            fuente(tamano)

    def crear_cancha():
        recursos.cancha = Field()

    def crear_jugadores():
        recursos.jugadores = (formacion("azul", recursos.cancha)
                              + formacion("rojo", recursos.cancha))

    def crear_pelota():
        recursos.pelota = Ball(*recursos.cancha.rect.center)

    def crear_partido():
        recursos.partido = Game(pantalla, recursos.cancha,
                                recursos.jugadores, recursos.pelota)

    return [
        ("Cargando tipografías...", preparar_fuentes),
        ("Cargando cancha...", crear_cancha),
        ("Cargando jugadores...", crear_jugadores),
        ("Preparando pelota...", crear_pelota),
        ("Preparando sonidos...", sonidos.iniciar),
        ("Inicializando partido...", crear_partido),
    ]


def avisar_al_navegador():
    """Le pide a la pagina que saque su pantalla de carga HTML.

    Solo existe cuando el juego corre con pygbag; en escritorio no hace nada.
    """
    try:
        import platform

        platform.window.splash_hide()
    except Exception:
        pass


async def main():
    pygame.init()
    pantalla = pygame.display.set_mode((s.ANCHO, s.ALTO))
    pygame.display.set_caption(s.TITULO)
    reloj = pygame.time.Clock()

    recursos = Recursos()
    carga = PantallaCarga(etapas_de_carga(pantalla, recursos))
    menu = Menu()
    instrucciones = Instrucciones()

    pantalla_actual = CARGA
    corriendo = True
    primer_frame = True

    while corriendo:
        # 1) Eventos: teclado, mouse, cerrar ventana.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif pantalla_actual == MENU:
                accion = menu.procesar_evento(evento)
                if accion == "jugar":
                    recursos.partido.reiniciar_partido()
                    pantalla_actual = JUEGO
                elif accion == "instrucciones":
                    pantalla_actual = INSTRUCCIONES
                elif accion == "salir":
                    corriendo = False

            elif pantalla_actual == INSTRUCCIONES:
                if instrucciones.procesar_evento(evento) == "menu":
                    pantalla_actual = MENU

            elif pantalla_actual == JUEGO:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pantalla_actual = MENU
                else:
                    recursos.partido.procesar_evento(evento)

        # 2) Estado + fisica (dt = segundos que duro el frame anterior).
        dt = reloj.tick(s.FPS) / 1000

        if pantalla_actual == CARGA:
            carga.actualizar(dt)
            carga.dibujar(pantalla)
            if carga.listo:
                pantalla_actual = MENU
        elif pantalla_actual == MENU:
            menu.actualizar(dt)
            menu.dibujar(pantalla)
        elif pantalla_actual == INSTRUCCIONES:
            instrucciones.actualizar(dt)
            instrucciones.dibujar(pantalla)
        else:
            recursos.partido.actualizar(dt)
            recursos.partido.dibujar()

        # 3) Mostrar el frame.
        pygame.display.flip()

        # Ya dibujamos algo: la pagina puede sacar su pantalla de carga HTML.
        if primer_frame:
            avisar_al_navegador()
            primer_frame = False

        # 4) Le devolvemos el control al navegador (obligatorio para pygbag).
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
