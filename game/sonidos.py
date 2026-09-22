"""Sonidos generados por codigo (no hay archivos de audio que descargar).

Armamos las ondas a mano con `math` y se las pasamos a pygame como bytes.
Ventaja para la web: 0 KB de descarga y 0 archivos extra en el build.
Si el navegador no deja usar el mixer, el juego sigue funcionando en silencio.
"""

import array
import math

import pygame

_sonidos = {}
_activo = False


def iniciar():
    """Prepara el mixer y crea los sonidos. Se llama una sola vez, al cargar."""
    global _activo
    try:
        pygame.mixer.init()
        _sonidos["golpe"] = _tono(220, 0.09, volumen=0.35, caida=28)
        _sonidos["rebote"] = _tono(140, 0.07, volumen=0.25, caida=34)
        _sonidos["gol"] = _arpegio([523, 659, 784], 0.12, volumen=0.4)
        _activo = True
    except Exception as error:  # audio bloqueado o no disponible: seguimos sin sonido
        print("Sin sonido:", error)
        _activo = False


def reproducir(nombre):
    if _activo and nombre in _sonidos:
        _sonidos[nombre].play()


def _muestras_por_segundo():
    frecuencia, _, _ = pygame.mixer.get_init()
    return frecuencia


def _tono(hz, segundos, volumen=0.4, caida=20):
    """Una nota que se apaga sola (la caida exponencial evita el 'clic')."""
    tasa = _muestras_por_segundo()
    total = int(tasa * segundos)
    muestras = array.array("h")
    for i in range(total):
        t = i / tasa
        amplitud = volumen * math.exp(-caida * t)
        muestras.append(int(32767 * amplitud * math.sin(2 * math.pi * hz * t)))
    return _a_sonido(muestras)


def _arpegio(notas, segundos_por_nota, volumen=0.4):
    tasa = _muestras_por_segundo()
    muestras = array.array("h")
    for hz in notas:
        total = int(tasa * segundos_por_nota)
        for i in range(total):
            t = i / tasa
            amplitud = volumen * math.exp(-6 * t)
            muestras.append(int(32767 * amplitud * math.sin(2 * math.pi * hz * t)))
    return _a_sonido(muestras)


def _a_sonido(muestras):
    """Convierte las muestras en un Sound, duplicandolas si el mixer es estereo."""
    _, _, canales = pygame.mixer.get_init()
    if canales > 1:
        estereo = array.array("h")
        for muestra in muestras:
            estereo.extend([muestra] * canales)
        muestras = estereo
    return pygame.mixer.Sound(buffer=muestras.tobytes())
