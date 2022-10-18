import pygame

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((0, 0, 0))



class Terrain(pygame.sprite.Sprite):
    def __init__(self, suface_Width, suface_Height, pos_Width, pos_Height):
        super(Terrain, self).__init__()
        self.surf = pygame.Surface((suface_Width, suface_Height))    
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(
            topleft=(
                pos_Width, pos_Height
            )
        )
        self.moving_up = True
    
    #Move the block up and down at a constant speed
    def update(self):
        if self.moving_up == True:
            self.rect.move_ip(0, -3)
        elif self.moving_up == False:
            self.rect.move_ip(0, 3)
        if self.rect.top == 575:
            self.moving_up = True
        if self.rect.top == 200:
            self.moving_up = False

    #Place block with mouse click
    def update2(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        if any(mouse_buttons):
            self.rect = self.surf.get_rect(
                center=(
                    mouse_pos
                )
            )
        screen.blit(self.surf, self.rect)


#Create blocks
surfaceOne = Terrain(200, 300, 0, 600)
surfaceTwo = Terrain(225, 350, 350, 500)
surfaceThree = Terrain(175, 50, 700, 500)
surfaceFour = Terrain(200, 300, 1000, 600)
surfaceFive = Terrain(100, 25, 0, 475)
surfaceSix = Terrain(100, 25, 150, 375)
surfaceSeven = Terrain(100, 175, 475, 425)
surfaceToCreate = Terrain(100, 25, 9999999, 99999999999)
surfaceToCreate.surf.fill((255, 255, 255))


#Add blocks to sprite group
terrain = pygame.sprite.Group()
terrain.add(surfaceOne)
terrain.add(surfaceTwo)
terrain.add(surfaceThree)
terrain.add(surfaceFour)
terrain.add(surfaceFive)
terrain.add(surfaceSix)
terrain.add(surfaceSeven)
terrain.add(surfaceToCreate)

#Added clock frame
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

    screen.fill((0,0,0))

    for obj in terrain:
        screen.blit(obj.surf,obj.rect)
    
    #Move surface three up and down
    surfaceThree.update()
    #Place the surface by mouse click
    surfaceToCreate.update2()

    pygame.display.flip()

    clock.tick(FRAME_RATE)