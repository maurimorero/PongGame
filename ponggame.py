
import pygame
from pygame.locals import *
import os
import sys
from random import randint

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "img"

def load_image(name, image_path, alpha=False):
    path = os.path.join(image_path, name)
    try:
        image = pygame.image.load(path)
    except:
        sys.exit(1)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

class Ball(pygame.sprite.Sprite):

    def __init__(self,numberOfPlayers):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("ball.png", IMG_DIR, alpha=True)
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
            elif self.numberOfPlayers == 3:
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

    def colision(self, objective):
        if self.rect.colliderect(objective.rect):
            if objective.type == "VerticalPaddle":
                self.speed[0] = -self.speed[0]
            elif objective.type == "HorizontalPaddle":
                self.speed[1] = -self.speed[1]


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x,y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type =type
        if self.type == "VerticalPaddle":
            self.image = load_image("VerticalPaddle.png", IMG_DIR, alpha=True)
        elif self.type == "HorizontalPaddle":
            self.image = load_image("HorizontalPaddle.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def human(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.top <= 0:
            self.rect.top = 0


def main():
    f = open('config.txt', 'r')
    line= f.readline()
    numberOfPlayers= int(line[-2:-1])

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MultiPlayer Pong")

    backgroud = load_image("background.jpg", IMG_DIR, alpha=False)
    ball = Ball(numberOfPlayers)
    player1 = Paddle(40,SCREEN_HEIGHT/2, "VerticalPaddle")
    if numberOfPlayers>1:
        player2 = Paddle(SCREEN_WIDTH - 40,SCREEN_HEIGHT/2,"VerticalPaddle")
    if numberOfPlayers>2:
        player3 = Paddle(SCREEN_WIDTH /2, 40,"HorizontalPaddle")
    if numberOfPlayers == 4:
        player4 = Paddle(SCREEN_WIDTH /2, 440, "HorizontalPaddle")

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)

    while True:
        clock.tick(40)
        player1.human()
        if numberOfPlayers > 1:
            player2.human()
        if numberOfPlayers > 2:
            player3.human()
        if numberOfPlayers == 4:
            player4.human()

        ball.update()
        ball.colision(player1)
        if numberOfPlayers > 1:
            ball.colision(player2)
        if numberOfPlayers > 2:
            ball.colision(player3)
        if numberOfPlayers == 4:
            ball.colision(player4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    player1.rect.centery -= 5
                elif event.key == K_s:
                    player1.rect.centery += 5
                if numberOfPlayers > 1:
                    if event.key == K_UP:
                        player2.rect.centery -= 5
                    elif event.key == K_DOWN:
                        player2.rect.centery += 5
                if numberOfPlayers > 2:
                    if event.key == K_r:
                        player3.rect.centerx -= 5
                    elif event.key == K_t:
                        player3.rect.centerx += 5
                if numberOfPlayers == 4:
                    if event.key == K_c:
                        player4.rect.centerx -= 5
                    elif event.key == K_v:
                        player4.rect.centerx += 5

                elif event.key == K_ESCAPE:
                    sys.exit(0)

        screen.blit(backgroud, (0, 0))
        screen.blit(ball.image, ball.rect)
        screen.blit(player1.image, player1.rect)
        if numberOfPlayers > 1:
            screen.blit(player2.image, player2.rect)
        if numberOfPlayers > 2:
            screen.blit(player3.image, player3.rect)
        if numberOfPlayers == 4:
            screen.blit(player4.image, player4.rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
