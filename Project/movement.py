from cgi import test
from turtle import Screen
import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



#Classes---------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75,150))
        self.surf.fill((255,255,255))
        # self.surf = pygame.image.load("{IMAGE PATH}").convert()
        # self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.grounded = False
        self.airTime = 0
        self.yVelocity = 0
    def updateYPos(self):
        self.rect.move_ip(0, self.yVelocity)
    #Movement
    # def update(self, pressed_keys):
        #For jumping, set self.yVelocity to a certain value when button is pressed?

class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        super(Terrain, self).__init__()
        self.surf = pygame.Surface((150,50))    
        self.surf.fill((0,255,0))
        #temporary terrain placement (create method with position, shape, and color as argument?)
        self.rect = self.surf.get_rect(
            topleft=(
                0, SCREEN_HEIGHT - 100
            )
        )

#Initialize Variables?-------
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

gAccel = 0.3

player = Player()
#temporary
testTerrain = Terrain()
    #Sprite Groups
all_sprites = pygame.sprite.Group()
gravity_obj = pygame.sprite.Group()
terrain = pygame.sprite.Group()
#add terrain to terrain group when generating terrain using a method?


    #Add to groups
all_sprites.add(player)
all_sprites.add(testTerrain)

gravity_obj.add(player)

#temporary
terrain.add(testTerrain)


clock = pygame.time.Clock()
FRAME_RATE = 60

running = True
#Game Loop-------------------
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False


    #GRAVITY
    for entity in gravity_obj:
        if pygame.sprite.spritecollideany(entity, terrain) and entity.grounded == False:
            entity.grounded = True
            entity.airtime = 0
            entity.yVelocity = 0
            if entity.rect.y < pygame.sprite.spritecollideany(entity, terrain).rect.bottom + 1:
                entity.rect.y = pygame.sprite.spritecollideany(entity, terrain).rect.top + 1 - entity.rect.h
        elif pygame.sprite.spritecollideany(entity, terrain) and entity.grounded == True:
            entity.airtime = 0
        else:
            entity.yVelocity += gAccel * entity.airTime
            entity.airTime += 1/FRAME_RATE


    screen.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player.updateYPos()
    pygame.display.flip()

    clock.tick(FRAME_RATE)