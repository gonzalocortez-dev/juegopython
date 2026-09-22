"""Punto de entrada del juego.

El bucle es asincrono (async/await) porque pygbag necesita devolverle el
control al navegador en cada frame. En la computadora funciona igual.
"""

import asyncio

import pygame

import settings as s
from game.game import Game


async def main():
    pygame.init()
    pantalla = pygame.display.set_mode((s.ANCHO, s.ALTO))
    pygame.display.set_caption(s.TITULO)
    reloj = pygame.time.Clock()

    juego = Game(pantalla)
    jugando = True

    while jugando:
        # 1) Eventos: teclado, mouse, cerrar ventana.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
            juego.procesar_evento(evento)

        # 2) Estado + fisica + colisiones + goles (dt = segundos del frame).
        dt = reloj.tick(s.FPS) / 1000
        juego.actualizar(dt)

        # 3) Dibujo.
        juego.dibujar()
        pygame.display.flip()

        # 4) Le devolvemos el control al navegador (obligatorio para pygbag).
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())
