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

## 1. Ejecutar en escritorio

Requiere Python 3.13 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 2. Ejecutar pygbag localmente (version navegador)

```bash
python -m pygbag main.py
```

Y abrir <http://localhost:8000>. La primera carga tarda unos segundos porque el
navegador descarga Python compilado a WebAssembly.

## 3. Generar el build web

```bash
python -m pygbag --build main.py
```

Los archivos publicables quedan en **`build/web/`**:

```
build/web/
├── index.html            <- pagina de entrada
├── futbol-de-mesa.apk    <- el juego empaquetado
├── futbol-de-mesa.tar.gz
└── favicon.png
```

Esa es la unica carpeta que hay que publicar (`build/web-cache/` es cache local
y no se sube). Para probarla como si fuera el sitio final:

```bash
python -m http.server 8000 --directory build/web
```

## 4. Publicar en GitHub Pages

El repo ya trae el workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml),
que genera el build y lo publica solo. Pasos:

1. Subir el proyecto a GitHub con la rama principal llamada `main`.
2. En GitHub: **Settings > Pages > Build and deployment > Source: GitHub Actions**.
3. Hacer push a `main` (o correr el workflow a mano desde la pestana **Actions**).
4. Cuando el workflow termina, el juego queda en:
   `https://<usuario>.github.io/<repositorio>/`

El resultado es un sitio estatico: quien lo abre **no necesita instalar Python**.

Si se prefiere publicar a mano, en [`web/README.md`](web/README.md) esta la
alternativa usando la rama `gh-pages`.

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
├── web/README.md      # como publicar el juego con pygbag
└── .github/workflows/deploy.yml   # build + deploy automatico a GitHub Pages
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
