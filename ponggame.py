#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Daniel Fuentes B.
# Licencia: X11/MIT license http://www.opensource.org/licenses/mit-license.php
# https://www.pythonmania.net/es/2010/04/07/tutorial-pygame-3-un-videojuego/

# ---------------------------
# Importacion de los módulos
# ---------------------------

import pygame
from pygame.locals import *
import os
import sys
from random import randint

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "imagenes"

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:


class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"

    def __init__(self,numberOfPlayers):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.centery = SCREEN_HEIGHT / 2
        self.numberOfPlayers = numberOfPlayers

        randomValue = randint(1,5)
        if randomValue == 1:
            self.speed = [3, -3]
        elif randomValue == 2:
            self.speed = [-3, -3]
        elif randomValue == 3:
            self.speed = [-3, 3]
        elif randomValue == 4:
            self.speed = [3, 3]
        else:
            self.speed = [3, 3]

    def update(self):
        if self.rect.left < 0:
            self.__init__(self.numberOfPlayers)
            pygame.time.delay(2500)
        if self.rect.right > SCREEN_WIDTH:
            if self.numberOfPlayers == 1:
                self.speed[0] = -self.speed[0]
            elif self.numberOfPlayers == 2:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
            elif self.numberOfPlayers == 3:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
            elif self.numberOfPlayers ==4:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
        if self.rect.top < 0:
            if self.numberOfPlayers == 1:
                self.speed[1] = -self.speed[1]
            elif self.numberOfPlayers == 2:
                self.speed[1] = -self.speed[1]
            elif self.numberOfPlayers ==3:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
            elif self.numberOfPlayers ==4:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
        if self.rect.bottom > SCREEN_HEIGHT:
            if self.numberOfPlayers == 1:
                self.speed[1] = -self.speed[1]
            elif self.numberOfPlayers == 2:
                self.speed[1] = -self.speed[1]
            elif self.numberOfPlayers == 3:
                self.speed[1] = -self.speed[1]
            elif self.numberOfPlayers ==4:
                self.__init__(self.numberOfPlayers)
                pygame.time.delay(2500)
        self.rect.move_ip((self.speed[0], self.speed[1]))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            if objetivo.type == "VerticalPaddle":
                self.speed[0] = -self.speed[0]
            elif objetivo.type == "HorizontalPaddle":
                self.speed[1] = -self.speed[1]


class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"

    def __init__(self, x,y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type =type
        if self.type == "VerticalPaddle":
            self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        elif self.type == "HorizontalPaddle":
            self.image = load_image("paleta1.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def humano(self):
        # Controlar que la paleta no salga de la pantalla
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

    def cpu(self, objetivo):
        self.rect.centery = objetivo.rect.centery
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0

# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    f = open('config.txt', 'r')
    line= f.readline()
    numberOfPlayers= int(line[-2:-1])
    #print(numberOfPlayers)

    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ejemplo de un Pong Simple")

    # cargamos los objetos
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    bola = Pelota(numberOfPlayers)
    jugador1 = Paleta(40,SCREEN_HEIGHT/2, "VerticalPaddle")
    if numberOfPlayers>1:
        jugador2 = Paleta(SCREEN_WIDTH - 40,SCREEN_HEIGHT/2,"VerticalPaddle")
    if numberOfPlayers>2:
        jugador3 = Paleta(SCREEN_WIDTH /2, 40,"HorizontalPaddle")
    if numberOfPlayers == 4:
        jugador4 = Paleta(SCREEN_WIDTH /2, 440, "HorizontalPaddle")

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    # el bucle principal del juego
    while True:
        clock.tick(40)
        # Obtenemos la posicon del mouse
        pos_mouse = pygame.mouse.get_pos()
        mov_mouse = pygame.mouse.get_rel()

        # Actualizamos los obejos en pantalla
        jugador1.humano()
        #jugador2.humano()
        #jugador3.humano()
        #jugador4.humano()
        if numberOfPlayers > 1:
            jugador2.humano()
        if numberOfPlayers > 2:
            jugador3.humano()
        if numberOfPlayers == 4:
            jugador4.humano()

        bola.update()

        # Comprobamos si colisionan los objetos
        bola.colision(jugador1)
        #bola.colision(jugador2)
        #bola.colision(jugador3)
        #bola.colision(jugador4)
        if numberOfPlayers > 1:
            bola.colision(jugador2)
        if numberOfPlayers > 2:
            bola.colision(jugador3)
        if numberOfPlayers == 4:
            bola.colision(jugador4)

        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:

                #jugador1
                if event.key == K_w:
                    jugador1.rect.centery -= 5
                elif event.key == K_s:
                    jugador1.rect.centery += 5

                #jugador2
                if event.key == K_UP:
                    jugador2.rect.centery -= 5
                elif event.key == K_DOWN:
                    jugador2.rect.centery += 5

                # jugador3
                if event.key == K_r:
                    jugador3.rect.centerx -= 5
                elif event.key == K_t:
                    jugador3.rect.centerx += 5

                # jugador4
                if event.key == K_c:
                    jugador4.rect.centerx -= 5
                elif event.key == K_v:
                    jugador4.rect.centerx += 5

                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    jugador2.rect.centery += 0
                elif event.key == K_DOWN:
                    jugador2.rect.centery += 0

            # Si el mouse no esta quieto mover la paleta a su posicion
            #elif mov_mouse[1] != 0:
            #   jugador1.rect.centery = pos_mouse[1]

        # actualizamos la pantalla
        screen.blit(fondo, (0, 0))
        screen.blit(bola.image, bola.rect)
        screen.blit(jugador1.image, jugador1.rect)
        #screen.blit(jugador2.image, jugador2.rect)
        #screen.blit(jugador3.image, jugador3.rect)
        #screen.blit(jugador4.image, jugador4.rect)
        if numberOfPlayers > 1:
            screen.blit(jugador2.image, jugador2.rect)
        if numberOfPlayers > 2:
            screen.blit(jugador3.image, jugador3.rect)
        if numberOfPlayers == 4:
            screen.blit(jugador4.image, jugador4.rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
