# Futbol de Mesa

Juego 2D de futbol de mesa por turnos (humano vs CPU) hecho con **Python + pygame-ce**,
pensado como demostracion educativa para alumnos de 3.º y 4.º año de escuela tecnica.
El mismo codigo corre en la computadora y en el navegador (con **pygbag**).

## Como se juega

- Vos sos el equipo **azul** (izquierda), la CPU es el **rojo** (derecha).
- **Click en una ficha azul** para seleccionarla (queda con un anillo amarillo).
- **Mover el mouse** para apuntar: aparece una flecha y una barra de potencia
  (cuanto mas lejos del jugador, mas fuerte el tiro).
- **Segundo click** para lanzar la ficha: al chocar, empuja la pelota.
- Cuando todo se detiene, juega la CPU.
- Gana el primero que llega a **3 goles**. Al terminar, **R** reinicia el partido.

## Instalacion

Requiere Python 3.13 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Jugarlo en el navegador

```bash
pygbag .
# abrir http://localhost:8000
```

Mas detalles (build y publicacion) en [`web/README.md`](web/README.md).

## Estructura del proyecto

```
futbol-de-mesa/
├── main.py            # bucle principal del juego (game loop)
├── settings.py        # constantes: tamanos, colores, fisica, reglas
├── game/
│   ├── field.py       # la cancha: medidas, dibujo y deteccion de gol
│   ├── ball.py        # la pelota: velocidad, friccion y rebotes
│   ├── player.py      # las fichas de cada equipo y la formacion inicial
│   ├── ai.py          # la IA del equipo rojo
│   └── game.py        # turnos, colisiones, marcador y dibujo del partido
├── assets/            # imagenes y sonidos (vacio: todo se dibuja con pygame)
└── web/README.md      # como publicar el juego con pygbag
```

## El game loop

Todo juego repite los mismos pasos ~60 veces por segundo (`main.py`):

1. Procesar eventos (mouse, teclado, cerrar ventana).
2. Actualizar el estado (de quien es el turno, si hubo gol).
3. Actualizar la fisica (posicion, velocidad, friccion).
4. Detectar colisiones (fichas entre si y contra los bordes).
5. Comprobar goles.
6. Dibujar.
7. Esperar para mantener 60 FPS.

## La fisica, en dos ideas

**Movimiento con friccion** (`ball.py`, `player.py`): cada ficha tiene una
posicion y una velocidad, ambas `pygame.Vector2`.

```python
self.pos += self.vel * dt          # se mueve
self.vel *= FRICCION ** (dt * FPS) # y se va frenando
```

**Choque entre dos circulos** (`game.py`, funcion `_chocar`): si la distancia
entre los centros es menor que la suma de los radios, se estan tocando.
Entonces se separan y se intercambia velocidad en la direccion que los une
(la "normal" del choque). La pelota tiene menos masa que los jugadores, por eso
sale disparada.

## Ideas para experimentar en clase

Casi todo se cambia tocando un solo numero en `settings.py`:

- `FRICCION`: 0.999 es una cancha de hielo, 0.94 es una alfombra.
- `GOLES_PARA_GANAR`, `JUGADORES_POR_EQUIPO`, `ALTO_ARCO`.
- `FUERZA_POR_PIXEL`: que tan fuertes son los tiros.
- En `ai.py`, el `random.uniform(-7, 7)` es la punteria de la CPU:
  achicarlo la hace mas dificil.

Ejercicios propuestos:

1. Agregar un sonido al patear (`assets/sounds/`).
2. Que el arquero no pueda salir del area.
3. Limitar el tiempo para apuntar.
4. Modo 2 jugadores en la misma computadora (sacar la IA).
