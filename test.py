import pygame, sys
from pygame.locals import *

bgImg = "data/img/overallBG.jpg"
ball = "data/img/ball.png"

pygame.init()
screen = pygame.display.set_mode((800,600),0,32)
background = pygame.image.load(bgImg).convert()
mouse_c = pygame.image.load(ball).convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
    
    screen.blit(background, (0,0))
    
    x,y = pygame.mouse.get_pos()
    x -= mouse_c.get_width()/2
    y -= mouse_c.get_height()/2
    screen.blit(mouse_c, (x,y))
    
    pygame.display.update()
    