import pygame
import random

pygame.init()
clock = pygame.time.Clock()
# Display 0 -> sets the display monitor to primary display instead of same display as code
screen = pygame.display.set_mode((1440,900),0,0,0)
pygame.display.set_caption('Food Invaders')
bg_surface = pygame.image.load('Background/Artboard 1.png')


class Lea (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Invader/Lea.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (550,780))
        self.speed = 0
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.speed < -20:
                self.speed = -20
            else:
                if self.speed > -4:
                    self.speed = -4
                else:
                    self.speed = self.speed * 1.1
            self.rect.x = self.rect.x + self.speed
        if keys[pygame.K_RIGHT]:
            if self.speed > 20:
                self.speed = 20
            else:
                if self.speed < 4:
                    self.speed = 4
                else:
                    self.speed = self.speed * 1.1
            self.rect.x = self.rect.x + self.speed
        # if self.rect.right < 0:
        #     self.rect.left = 1440

        # above section works, but with below section i'm trying to allow half of the bunny to be on 1 side
        # while the out of screen portion is on the other side.
        if self.rect.left < 0:
            copy = self.image.copy()
            screen.blit(copy,(500,500))
            self.rect = self.rect + copy


        if self.rect.left > 1440:
            self.rect.right = 0

    def update(self):
        self.player_input()

class David (Lea):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Invader/David.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (750,780))

class Andijvie (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Victim/Andijvie.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = ((random.randint(200, 1240)), 200))

    # def update(self):
    #     # self.destory()

    # def destroy(self):
    #     if self.rect.y <= 900:
    #         self.kill()

class Witlof (Andijvie):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Victim/Witlof.png').convert_alpha()

invaders = pygame.sprite.Group()
invaders.add(David(), Lea())

food = pygame.sprite.Group()
food.add(Andijvie(), Witlof())

game_active = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_active:
        screen.blit(bg_surface,(0,0))
        invaders.draw(screen)
        invaders.update()
        food.draw(screen)
        food.update()



    else: # start/end game screen
        screen.fill((94,129,162))

    clock.tick(140)
    pygame.display.update()
pygame.quit()