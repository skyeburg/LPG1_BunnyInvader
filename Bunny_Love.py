import pygame
from sys import exit
import random
import math

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
        if self.rect.right < 0:
            self.rect.left = 1440
        elif self.rect.left > 1440:
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
        self.rect = self.image.get_rect(midbottom = ((random.randint(200, 1240)), 0))
        self.rect = self.rect.scale_by(0.4)

    def update(self):
        global current_time
        self.rect.y += 5 + (math.sqrt(current_time/2000))

class Witlof (Andijvie):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Victim/Witlof.png').convert_alpha()

class Ground (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((1440, 900))
        self.surface.fill('Red')
        self.image = self.surface
        self.rect = self.image.get_rect(topleft = (0,900))

def collision():
    # Score
    global score_eaten
    global game_active
    if pygame.sprite.spritecollide(lea.sprite, witlof, True) or pygame.sprite.spritecollide(david.sprite, andijvie, True):
        score_eaten += 1
        eating_sound.play()
    score_surf = font2.render(f'Score: {score_eaten}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (200, 85))
    screen.blit(score_surf, score_rect)

    # Life total
    for position in nolife_positions: screen.blit(nolife_surf, position)
    for position in life_positions: screen.blit(fulllife_surf, position)
    if pygame.sprite.spritecollide(ground.sprite, witlof, True) or pygame.sprite.spritecollide(ground.sprite, andijvie, True) or pygame.sprite.spritecollide(lea.sprite, andijvie, True) or pygame.sprite.spritecollide(david.sprite, witlof, True): 
        life_positions.pop()
        hit_sound.play()
        if life_positions == []: 
            game_active = False
            game_over_sound.play()

def add_food():
    type = random.randint(0,1)
    if type == 0:
        andijvie.add(Andijvie())
    else: witlof.add(Witlof())

# life total
fulllife_surf = pygame.transform.scale_by(pygame.image.load('Life/Full hearth.png'),0.1)
nolife_surf = pygame.transform.scale_by(pygame.image.load('Life/Empty hearth.png'),0.1)
life_positions = [(1100,50), (1200,50), (1300,50)]
nolife_positions = [(1100,50), (1200,50), (1300,50)]

# Basics
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1440,900),0,0,0)
# Display 0 -> sets the display monitor to primary display instead of same display as code
pygame.display.set_caption('Bunny Love')
bg_surface = pygame.image.load('Background/Artboard 1.png')
game_active = False
font1 = pygame.font.Font('Font/Pacifico-Regular.ttf',25)
font2 = pygame.font.Font('Font/Pacifico-Regular.ttf',50)
font3 = pygame.font.Font('Font/Pacifico-Regular.ttf',100)
score_eaten = 0
bg_music = pygame.mixer.Sound("Audio\In The Mood For Noune.mp3")
bg_music.set_volume(1)
bg_music.play(loops = -1)
hit_sound = pygame.mixer.Sound('Audio\hit.wav')
eating_sound = pygame.mixer.Sound('Audio\munching-food.mp3')
game_over_sound = pygame.mixer.Sound('Audio\game_over.wav')


# Groups
david = pygame.sprite.GroupSingle()
david.add(David())

lea = pygame.sprite.GroupSingle()
lea.add(Lea())

andijvie = pygame.sprite.Group()
witlof = pygame.sprite.Group()

ground = pygame.sprite.GroupSingle()
ground.add(Ground())

# spawn timer
last_spawn_time = 0
spawn_interval = 2500

# game Loop
while True:
    current_time = pygame.time.get_ticks()
    time_since_last_spawn = current_time - last_spawn_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if time_since_last_spawn >= spawn_interval:
        add_food()
        last_spawn_time = current_time
        if spawn_interval > 800: spawn_interval -= 50

    if game_active:
        screen.blit(bg_surface,(0,0))

        lea.draw(screen)
        lea.update()
        david.draw(screen)
        david.update()
        andijvie.draw(screen)
        andijvie.update()
        witlof.draw(screen)
        witlof.update()
        ground.draw(screen)
        ground.update()
        fps = font1.render(f'{int(pygame.time.Clock.get_fps(clock))}', False, (186,208,222))
        fps_rect = fps.get_rect(center = (35, 20))
        screen.blit(fps, fps_rect)
        collision()

    # Start/End    
    else:
        screen.fill((94,129,162))
        end_image = pygame.image.load('Background\BG end screen.png')
        screen.blit(end_image, (218,000))
        score_message = font2.render(f'Score: {score_eaten}',False,(0,0,0))
        score_message_rect = score_message.get_rect(center = (650,100))

        if score_eaten == 0:
            message = 'FOOD DEVOURERS'
        else:
            screen.blit(score_message, score_message_rect)
            message = '  Press space to try again  '
        title = font3.render(message, False, (0, 0, 0), (94,129,162))
        title_rect = title.get_rect(center = (725, 825))
        screen.blit(title, title_rect)

        # Reset
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                life_positions = [(1100,50), (1200,50), (1300,50)]
                score_eaten = 0
                game_active = True
                andijvie.empty()
                witlof.empty()
                spawn_interval = 2500

    pygame.display.update()
    clock.tick(140)

pygame.quit()