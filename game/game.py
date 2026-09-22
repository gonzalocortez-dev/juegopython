"""El partido: junta todas las piezas y maneja turnos, fisica y dibujo."""

import pygame

import settings as s
from game import ai
from game.ball import Ball
from game.field import Field
from game.player import formacion

# Estados posibles del partido (un string simple alcanza para entenderlo).
APUNTANDO = "apuntando"     # turno del humano: elige ficha y direccion
PENSANDO = "pensando"       # la CPU "piensa" un instante antes de tirar
MOVIENDO = "moviendo"       # hay fichas en movimiento, nadie puede tirar
GOL = "gol"                 # pausa corta para mostrar el gol
FIN = "fin"                 # alguien llego a 3 goles


class Game:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.cancha = Field()
        self.fuente_grande = pygame.font.Font(None, 64)
        self.fuente = pygame.font.Font(None, 34)
        self.fuente_chica = pygame.font.Font(None, 26)
        self.reiniciar_partido()

    # ------------------------------------------------------------------
    # Preparacion
    # ------------------------------------------------------------------

    def reiniciar_partido(self):
        self.goles = {"azul": 0, "rojo": 0}
        self.turno = "azul"
        self.estado = APUNTANDO
        self.temporizador = 0.0
        self.mensaje = ""
        self.jugadores = formacion("azul", self.cancha) + formacion("rojo", self.cancha)
        self.pelota = Ball(*self.cancha.rect.center)
        self.seleccionado = None

    def sacar_del_medio(self):
        """Vuelve todo a la posicion inicial (despues de un gol)."""
        for jugador in self.jugadores:
            jugador.volver_al_inicio()
        self.pelota.pos.update(self.cancha.rect.center)
        self.pelota.vel.update(0, 0)
        self.seleccionado = None

    def equipo(self, nombre):
        return [j for j in self.jugadores if j.equipo == nombre]

    # ------------------------------------------------------------------
    # 1) Eventos
    # ------------------------------------------------------------------

    def procesar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and self.estado == FIN:
            self.reiniciar_partido()
            return

        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
        if self.estado != APUNTANDO or self.turno != "azul":
            return

        mouse = pygame.Vector2(evento.pos)
        tocado = self._jugador_en(mouse, "azul")

        if tocado is not None:
            self._seleccionar(tocado)
        elif self.seleccionado is not None:
            self._tirar(mouse)

    def _jugador_en(self, punto, equipo):
        for jugador in self.equipo(equipo):
            if jugador.contiene(punto):
                return jugador
        return None

    def _seleccionar(self, jugador):
        for otro in self.jugadores:
            otro.seleccionado = False
        jugador.seleccionado = True
        self.seleccionado = jugador

    def _tirar(self, objetivo):
        """Lanza la ficha seleccionada hacia donde apunta el mouse."""
        direccion = objetivo - self.seleccionado.pos
        if direccion.length() == 0:
            return
        fuerza = min(direccion.length(), s.DISTANCIA_MAXIMA_TIRO) * s.FUERZA_POR_PIXEL
        self.seleccionado.lanzar(direccion.normalize(), fuerza)
        self.seleccionado.seleccionado = False
        self.seleccionado = None
        self.estado = MOVIENDO

    # ------------------------------------------------------------------
    # 2) Actualizacion del estado y de la fisica
    # ------------------------------------------------------------------

    def actualizar(self, dt):
        if self.estado == FIN:
            return

        if self.estado == GOL:
            self.temporizador -= dt
            if self.temporizador <= 0:
                self.sacar_del_medio()
                self.mensaje = ""
                self.estado = APUNTANDO if self.turno == "azul" else PENSANDO
                self.temporizador = 0.7
            return

        if self.estado == PENSANDO:
            self.temporizador -= dt
            if self.temporizador <= 0:
                self._turno_cpu()
            return

        self._mover_fichas(dt)
        self._resolver_colisiones()

        if self.estado == MOVIENDO:
            equipo_que_convirtio = self.cancha.revisar_gol(self.pelota)
            if equipo_que_convirtio:
                self._festejar_gol(equipo_que_convirtio)
            elif self._todo_detenido():
                self._cambiar_turno()

    def _mover_fichas(self, dt):
        for jugador in self.jugadores:
            jugador.actualizar(dt, self.cancha)
        self.pelota.actualizar(dt, self.cancha)

    def _todo_detenido(self):
        return self.pelota.detenida and all(j.detenido for j in self.jugadores)

    def _cambiar_turno(self):
        if self.turno == "azul":
            self.turno = "rojo"
            self.estado = PENSANDO
            self.temporizador = 0.7
        else:
            self.turno = "azul"
            self.estado = APUNTANDO

    def _turno_cpu(self):
        jugador, direccion, fuerza = ai.elegir_tiro(
            self.equipo("rojo"), self.pelota, self.cancha)
        jugador.lanzar(direccion, fuerza)
        self.estado = MOVIENDO

    def _festejar_gol(self, equipo_que_convirtio):
        self.goles[equipo_que_convirtio] += 1
        self.mensaje = "GOL AZUL" if equipo_que_convirtio == "azul" else "GOL CPU"
        # Saca el equipo al que le convirtieron.
        self.turno = "rojo" if equipo_que_convirtio == "azul" else "azul"

        if self.goles[equipo_que_convirtio] >= s.GOLES_PARA_GANAR:
            self.estado = FIN
            self.mensaje = ("GANASTE" if equipo_que_convirtio == "azul"
                            else "GANO LA CPU")
        else:
            self.estado = GOL
            self.temporizador = 1.5

    # ------------------------------------------------------------------
    # 3) Colisiones entre fichas (choque elastico simplificado)
    # ------------------------------------------------------------------

    def _resolver_colisiones(self):
        fichas = self.jugadores + [self.pelota]
        for i, a in enumerate(fichas):
            for b in fichas[i + 1:]:
                _chocar(a, b)

    # ------------------------------------------------------------------
    # 4) Dibujo
    # ------------------------------------------------------------------

    def dibujar(self):
        self.cancha.dibujar(self.pantalla)

        for jugador in self.jugadores:
            jugador.dibujar(self.pantalla)
        self.pelota.dibujar(self.pantalla)

        if self.seleccionado is not None:
            self._dibujar_mira()

        self._dibujar_marcador()
        self._dibujar_mensaje()

    def _dibujar_mira(self):
        """Flecha de apuntado y barra de potencia de la ficha seleccionada."""
        mouse = pygame.Vector2(pygame.mouse.get_pos())
        origen = self.seleccionado.pos
        direccion = mouse - origen
        if direccion.length() < 1:
            return

        largo = min(direccion.length(), s.DISTANCIA_MAXIMA_TIRO)
        punta = origen + direccion.normalize() * largo
        _dibujar_flecha(self.pantalla, origen, punta, s.AMARILLO)

        potencia = largo / s.DISTANCIA_MAXIMA_TIRO
        barra = pygame.Rect(origen.x - 30, origen.y + s.RADIO_JUGADOR + 12, 60, 8)
        pygame.draw.rect(self.pantalla, s.NEGRO, barra, border_radius=4)
        pygame.draw.rect(self.pantalla, s.AMARILLO,
                         (barra.x, barra.y, barra.width * potencia, barra.height),
                         border_radius=4)

    def _dibujar_marcador(self):
        pygame.draw.rect(self.pantalla, s.NEGRO, (0, 0, s.ANCHO, s.MARGEN_SUPERIOR - 10))

        marcador = f"{self.goles['azul']}  -  {self.goles['rojo']}"
        texto = self.fuente_grande.render(marcador, True, s.BLANCO)
        self.pantalla.blit(texto, texto.get_rect(center=(s.ANCHO // 2, 35)))

        azul = self.fuente.render("AZUL (vos)", True, s.AZUL_CLARO)
        rojo = self.fuente.render("ROJO (CPU)", True, s.ROJO)
        self.pantalla.blit(azul, (40, 22))
        self.pantalla.blit(rojo, rojo.get_rect(topright=(s.ANCHO - 40, 22)))

        if self.estado == FIN:
            turno, color = "Presiona R para jugar de nuevo", s.AMARILLO
        elif self.turno == "azul" and self.estado == APUNTANDO:
            turno, color = "TU TURNO", s.AZUL_CLARO
        elif self.turno == "rojo":
            turno, color = "TURNO CPU", s.ROJO
        else:
            turno, color = "...", s.BLANCO

        texto_turno = self.fuente.render(turno, True, color)
        self.pantalla.blit(texto_turno,
                           texto_turno.get_rect(center=(s.ANCHO // 2, 68)))

        ayuda = "Click en una ficha azul para elegirla y otro click para disparar"
        texto_ayuda = self.fuente_chica.render(ayuda, True, s.BLANCO)
        self.pantalla.blit(texto_ayuda,
                           texto_ayuda.get_rect(center=(s.ANCHO // 2, s.ALTO - 18)))

    def _dibujar_mensaje(self):
        if not self.mensaje:
            return
        texto = self.fuente_grande.render(self.mensaje, True, s.AMARILLO)
        rect = texto.get_rect(center=(s.ANCHO // 2, s.ALTO // 2))
        pygame.draw.rect(self.pantalla, s.NEGRO, rect.inflate(60, 30), border_radius=12)
        self.pantalla.blit(texto, rect)


def _chocar(a, b):
    """Separa dos fichas superpuestas e intercambia velocidad en el eje del choque."""
    delta = b.pos - a.pos
    distancia = delta.length()
    suma_radios = a.radio + b.radio
    if distancia == 0 or distancia >= suma_radios:
        return

    normal = delta / distancia

    # 1) Las despegamos para que no queden pegadas (segun su masa).
    superposicion = suma_radios - distancia
    total = a.masa + b.masa
    a.pos -= normal * superposicion * (b.masa / total)
    b.pos += normal * superposicion * (a.masa / total)

    # 2) Solo importa la velocidad con la que se acercan (a lo largo de la normal).
    velocidad_relativa = (b.vel - a.vel).dot(normal)
    if velocidad_relativa > 0:
        return  # ya se estan separando

    impulso = -(1 + s.REBOTE_FICHAS) * velocidad_relativa / (1 / a.masa + 1 / b.masa)
    a.vel -= normal * (impulso / a.masa)
    b.vel += normal * (impulso / b.masa)


def _dibujar_flecha(pantalla, desde, hasta, color):
    pygame.draw.line(pantalla, color, desde, hasta, 4)
    direccion = hasta - desde
    if direccion.length() < 1:
        return
    direccion = direccion.normalize()
    izquierda = direccion.rotate(140) * 18
    derecha = direccion.rotate(-140) * 18
    pygame.draw.polygon(pantalla, color,
                        [hasta, hasta + izquierda, hasta + derecha])
