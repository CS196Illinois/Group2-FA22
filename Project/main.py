import pygame
import map
import movement
from cgi import test
from turtle import Screen
from math import sqrt as root
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_LSHIFT,
    K_RSHIFT,
)
pygame.init()


#Screen setup
#-----------------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
movement.SCREEN_HEIGHT = SCREEN_HEIGHT
movement.SCREEN_WIDTH = SCREEN_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0, 0, 0))
#-----------------------------


#Blocks for the map
#-----------------------------
surfaceOne = map.Terrain(200, 300, 0, 600)
surfaceTwo = map.Terrain(225, 350, 350, 500)
surfaceThree = map.Terrain(175, 50, 700, 500)
surfaceFour = map.Terrain(200, 300, 1000, 600)
surfaceFive = map.Terrain(100, 25, 0, 475)
surfaceSix = map.Terrain(100, 25, 150, 375)
surfaceSeven = map.Terrain(100, 175, 475, 425)
surfaceHitToWin = map.Terrain(100, 25, 1100, 350)
surfaceToCreate = map.Terrain(100, 25, 9999999, 99999999999)
surfaceToCreate.surf.fill((255, 255, 255))
#-----------------------------


gAccel = 6

player = movement.Player()


#Add to sprite group
#-----------------------------
all_sprites = pygame.sprite.Group()
all_sprites.add(surfaceOne)
all_sprites.add(surfaceTwo)
all_sprites.add(surfaceThree)
all_sprites.add(surfaceFour)
all_sprites.add(surfaceFive)
all_sprites.add(surfaceSix)
all_sprites.add(surfaceSeven)
all_sprites.add(surfaceHitToWin)
all_sprites.add(surfaceToCreate)
all_sprites.add(player)

gravity_obj = pygame.sprite.Group()
gravity_obj.add(player)

terrain = pygame.sprite.Group()
terrain.add(surfaceOne)
terrain.add(surfaceTwo)
terrain.add(surfaceThree)
terrain.add(surfaceFour)
terrain.add(surfaceFive)
terrain.add(surfaceSix)
terrain.add(surfaceSeven)
terrain.add(surfaceHitToWin)
terrain.add(surfaceToCreate)
#-----------------------------


#Score
#-----------------------------
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
green = (0, 255, 0)

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.display_surface = pygame.display.set_mode((0, 0))
        pygame.display.set_caption('Show Text')
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.score = 0
        self.text = self.font.render('Score: ' + str(self.score), True, green, black)
        self.textRect = self.text.get_rect()
        self.restarted = True

    def update(self, Player):
        if self.restarted == True:
            if Player.rect.right == 1200:
               self.score = self.score + 1
               self.text = self.font.render('Score: ' + str(self.score), True, green, black)
               self.restarted = False
#-----------------------------
score = Score()


clock = pygame.time.Clock()
FRAME_RATE = 60

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    for entity in gravity_obj:
        if pygame.sprite.spritecollideany(entity, terrain):
            obj = pygame.sprite.spritecollideany(entity, terrain).rect
            if entity.grounded == False:
                #Check if player is less than 50 units into the ground from the top (should be only when player lands on top of terrain)
                if entity.rect.right > obj.left and entity.rect.left < obj.right and entity.rect.bottom < obj.top + 50:
                    entity.grounded = True
                    entity.airTime = 0
                    entity.yVelocity = 0
                    entity.rect.y = obj.top + 1 - entity.rect.h
                #Check if player is more than 50 units into the ground from the top (should be only when player is not on terrain/on the side of the terrain)
                else:
                    #Check which side of terrain player is colliding with
                    #Right
                    if entity.rect.left < obj.right and entity.rect.left > obj.right - 10:
                        entity.rect.left = obj.right
                    #Left
                    if entity.rect.right > obj.left and entity.rect.right < obj.left + 10:
                        entity.rect.right = obj.left
            elif entity.grounded == True:
                entity.airTime = 0
        else:
            entity.grounded = False
            entity.yVelocity = entity.yVelocity + gAccel * entity.airTime
            entity.airTime += 1/FRAME_RATE

    screen.fill((0, 0, 0))
    
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player.updateYPos()

    for obj in terrain:
        screen.blit(obj.surf,obj.rect)
    
    score.display_surface.blit(score.text, score.textRect)

    #Increase score
    score.update(player)
    
    #Move surface three up and down
    surfaceThree.update()
    #Place the surface by mouse click
    surfaceToCreate.update2()


    pygame.display.flip()

    clock.tick(FRAME_RATE)

