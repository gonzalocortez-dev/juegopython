"""Constantes del juego.

Todo lo que se puede "tocar" para cambiar el juego (tamanos, colores,
velocidades) vive aca, asi los alumnos experimentan sin romper la logica.
"""

# --- Ventana ---
ANCHO = 1280
ALTO = 720
FPS = 60
TITULO = "Futbol de Mesa"

# --- Colores (R, G, B) ---
VERDE_CANCHA = (34, 139, 68)
VERDE_OSCURO = (28, 120, 58)
BLANCO = (245, 245, 245)
AZUL = (40, 110, 230)
AZUL_CLARO = (150, 190, 255)
ROJO = (220, 60, 60)
NEGRO = (20, 20, 20)
AMARILLO = (250, 220, 70)

# --- Cancha ---
MARGEN_X = 70          # espacio entre el borde de la ventana y la linea lateral
MARGEN_SUPERIOR = 80   # espacio reservado arriba para el marcador
MARGEN_INFERIOR = 40
ALTO_ARCO = 200        # alto de la boca del arco
PROFUNDIDAD_ARCO = 40  # cuanto "entra" el arco hacia afuera de la cancha

# --- Fichas (jugadores y pelota) ---
RADIO_JUGADOR = 22
RADIO_PELOTA = 12
JUGADORES_POR_EQUIPO = 5

# --- Fisica ---
FRICCION = 0.985        # cuanta velocidad conserva cada ficha en cada frame
VELOCIDAD_MINIMA = 8    # por debajo de esto la ficha se considera detenida
VELOCIDAD_MAXIMA = 1400 # limite de velocidad (pixeles por segundo)
REBOTE_PARED = 0.75     # energia conservada al chocar contra un borde
REBOTE_FICHAS = 0.95    # energia conservada al chocar dos fichas

# --- Disparo ---
FUERZA_POR_PIXEL = 5.5  # cuanta velocidad da cada pixel de "estiramiento" del tiro
DISTANCIA_MAXIMA_TIRO = 220  # mas lejos que esto el tiro ya no gana potencia

# --- Partido ---
GOLES_PARA_GANAR = 3
